#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2022 Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
#
# SPDX-License-Identifier: EUPL-1.2

"""
Migration script for the spotlights from the hifis.net website.
"""

import argparse
import os
import re
import glob
import logging
import base64
import magic

import yaml
import jwt

import asyncio
from postgrest import AsyncPostgrestClient

from mdparser.mdparser import SvHtmlParser


VERBOSE = False
DELETE_SPOTLIGHTS = False
UPDATE_IMPRINT = False
POSTGREST_URL = os.environ.get("POSTGREST_URL")
PGRST_JWT_SECRET = os.environ.get("PGRST_JWT_SECRET")
JWT_PAYLOAD = {"role": "rsd_admin"}
JWT_ALGORITHM = "HS256"
SPOTLIGHTS_DIR = "hifis.net/_spotlights"

ORGANISATIONS = {
    "Helmholtz Centre for Environmental Research (UFZ)": {
        "logo": "UFZ.svg",
        "ror": "000h6jb29",
    },
    "Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences": {
        "logo": "GFZ.svg",
        "ror": "04z8jg394",
    },
    "German Aerospace Center (DLR)": {
        "logo": "DLR.svg",
        "ror": "04bwf3e34",
    },
    "Alfred Wegener Institute for Polar and Marine Research (AWI)": {
        "logo": "AWI.svg",
        "ror": "032e6b942",
    },
    "Karlsruhe Institute of Technology (KIT)": {
        "logo": "KIT.svg",
        "ror": "04t3en479",
    },
    "CISPA Helmholtz Center for Information Security": {
        "logo": "CISPA.png",
        "ror": "02njgxr09",
    },
    "Helmholtz Centre for Heavy Ion Research (GSI)": {
        "logo": "GSI.svg",
        "ror": "02k8cbn47",
    },
    "Helmholtz Centre For Ocean Research Kiel (GEOMAR)": {
        "logo": "GEOMAR.jpg",
        "ror": "02h2x0161",
    },
    "Helmholtz-Zentrum Dresden-Rossendorf": {
        "logo": "HZDR.png",
        "ror": "01zy2cs03",
    },
    "Forschungszentrum Jülich": {
        "logo": "FZJ.svg",
        "ror": "02nv7yv05",
    },
    "Deutsches Elektronen-Synchrotron DESY": {
        "logo": "DESY.svg",
        "ror": "01js2sh04",
    },
}
MISSING_LOGOS = []

mime = magic.Magic(mime=True)


def get_md_without_front_matter(file):
    found = 0
    retlines = []

    with open(file, "r") as opened_file:
        alllines = opened_file.readlines()

        for line in alllines:
            if line.startswith("---"):
                found += 1
            elif found >= 2:
                retlines.append(line)

    raw_markdown = "".join(retlines)

    # Parse to remove html tags
    md_parser = SvHtmlParser()
    md_parser.feed(raw_markdown)

    md_parsed = md_parser.close().to_markdown()

    # Now split by code blocks
    md_split = md_parsed.split(r"```")
    if len(md_split) % 2 == 0:
        raise Exception("There was an error parsing markdown code blocks in %s" % file)

    # Remove line breaks inside paragraphs, because they would be rendered as <br>
    # Only every scond block, because we do not want to replace newlines in code blocks
    for i in range(0, len(md_split), 2):
        md_split[i] = re.sub(
            r"(?<=[\w., \(\)\[\]])(\n)(?=[\w., \(\)\[\]])", " ", md_split[i]
        )

    return "```".join(md_split)


def get_spotlights():
    files = glob.glob(SPOTLIGHTS_DIR + os.sep + "*.md")
    filtered = list(filter(lambda x: "_template.md" not in x, files))

    spotlights = []

    for file in filtered:
        with open(file, "r") as opened_file:
            try:
                logging.info("Preparing %s", file)
                # https://stackoverflow.com/a/34727830
                load_all = yaml.load_all(opened_file, Loader=yaml.FullLoader)

                metadata = next(load_all)
                metadata["description"] = get_md_without_front_matter(file)

                if metadata.get("name") is None:
                    raise Exception("Spotlight %s has no name" % file)

                spotlights.append(metadata)
            except yaml.YAMLError as exc:
                print(exc)

    return spotlights


def name_to_slug(name):
    remove_chars = name.replace(" ", "-").replace("+", "").lower()

    # remove multiple '-'
    return re.sub(r"\-+", "-", remove_chars)


def org_name_to_slug(name):
    name = (
        name.replace(" ", "-")
        .replace("ä", "a")
        .replace("ö", "o")
        .replace("ü", "u")
        .replace("ß", "ss")
        .lower()
    )
    name = "".join(char for char in name if (char.isalnum() or char == "-"))
    return name


async def slug_to_id(client, slug):
    res = await client.from_("software").select("id", "slug").eq("slug", slug).execute()

    if len(res.data) > 0:
        return res.data[0].get("id")

    return None


def convert_spotlight_to_software(spotlight):
    name = spotlight.get("name")
    doi = spotlight.get("doi")
    description = spotlight.get("description", "")

    assert len(description) <= 10000

    software = {
        "slug": name_to_slug(name),
        "brand_name": name,
        "is_published": True,
        "short_statement": spotlight.get("excerpt", "")[:300],
        "description": description,
    }

    if doi is None:
        # nothing more to do
        return software

    if type(doi) == list:
        logging.warning(
            "Multiple DOIs are not supported. " "Consider adding %s as a project.",
            name,
        )
    elif not doi.startswith("10."):
        logging.warning("Spotlight %s: %s is not a valid DOI.", name, doi)
    else:
        software["concept_doi"] = doi

    return software


async def spotlight_exists(client, spotlight) -> bool:
    name = spotlight.get("name")
    slug = name_to_slug(name)
    software_id = await slug_to_id(client, slug)
    if software_id is not None:
        return True
    else:
        return False


async def remove_spotlight(client, spotlight):
    name = spotlight.get("name")
    slug = name_to_slug(name)
    software_id = await slug_to_id(client, slug)

    if software_id is not None:
        # remove related entries
        res = (
            await client.from_("maintainer_for_software")
            .delete()
            .eq("software", software_id)
            .execute()
        )

        res = (
            await client.from_("release")
            .select("id")
            .eq("software", software_id)
            .execute()
        )

        for rel in res.data:
            res = (
                await client.from_("release_content")
                .delete()
                .eq("release_id", rel.get("id"))
                .execute()
            )

        res = (
            await client.from_("release").delete().eq("software", software_id).execute()
        )

        res = (
            await client.from_("repository_url")
            .delete()
            .eq("software", software_id)
            .execute()
        )

        res = (
            await client.from_("license_for_software")
            .delete()
            .eq("software", software_id)
            .execute()
        )

        res = (
            await client.from_("contributor")
            .delete()
            .eq("software", software_id)
            .execute()
        )

        res = (
            await client.from_("keyword_for_software")
            .delete()
            .eq("software", software_id)
            .execute()
        )

        res = (
            await client.from_("software_for_organisation")
            .delete()
            .eq("software", software_id)
            .execute()
        )

    logging.info("Remove %s", name)

    res = await client.from_("software").delete().eq("slug", slug).execute()

    logging.info(res.data)


async def add_spotlight(client, spotlight):
    name = spotlight.get("name")

    logging.info("Add %s", name)

    sw_data = convert_spotlight_to_software(spotlight)

    logging.info(sw_data)

    res = await client.from_("software").insert(sw_data).execute()

    logging.info(res.data)


async def add_spotlight_urls(client, spotlight):
    name = spotlight.get("name")
    slug = name_to_slug(name)

    platforms = spotlight.get("platforms", [])

    if len(platforms) == 0:
        logging.info("Spotlight %s has no platforms", name)
        return

    found_github = None
    found_gitlab = None
    found_webpage = None
    to_add = None
    to_update = None

    for plat in platforms:
        ptype = plat.get("type")

        if ptype == "gitlab":
            found_gitlab = plat.get("link_as")
        if ptype == "github":
            found_github = plat.get("link_as")
        if ptype == "webpage":
            found_webpage = plat.get("link_as")

    software_id = await slug_to_id(client, slug)

    # first check for GitLab as we prefer it over GitHub and only one entry
    # can be made in the RSD
    if found_gitlab is not None:
        to_add = {
            "software": software_id,
            "code_platform": "gitlab",
            "url": found_gitlab,
        }
    elif found_github is not None:
        to_add = {
            "software": software_id,
            "code_platform": "github",
            "url": found_github,
        }

    if to_add is not None:
        logging.info("Add repository URL for %s", name)
        res = await client.from_("repository_url").insert(to_add).execute()
        logging.info(res.data)

    if found_webpage is not None:
        to_update = {
            "get_started_url": found_webpage,
        }
        logging.info("Add get started URL for %s", name)
        res = (
            await client.from_("software")
            .update(to_update)
            .eq("id", software_id)
            .execute()
        )
        logging.info(res.data)


async def add_license(client, spotlight):
    slicense = spotlight.get("license")

    if slicense is None or len(slicense) == 0:
        # no license specified
        return

    name = spotlight.get("name")
    slug = name_to_slug(name)
    software_id = await slug_to_id(client, slug)

    logging.info("Add license for %s", name)

    res = (
        await client.from_("license_for_software")
        .insert({"software": software_id, "license": slicense})
        .execute()
    )

    logging.info(res.data)


async def get_id_for_keyword(client, keyword):
    res = (
        await client.from_("keyword")
        .select("id", "value")
        .eq("value", keyword)
        .execute()
    )

    if len(res.data) > 0:
        return res.data[0].get("id")

    return None


async def add_keywords(client, spotlight):
    keywords = spotlight.get("keywords")

    if keywords is None or len(keywords) == 0:
        # no keyword specified
        return

    name = spotlight.get("name")
    slug = name_to_slug(name)
    software_id = await slug_to_id(client, slug)

    logging.info("Add keywords for %s", name)

    for keyword in keywords:
        kw_id = await get_id_for_keyword(client, keyword)

        if kw_id is None:
            logging.info("Adding keyword %s" % keyword)

            res = await client.from_("keyword").insert({"value": keyword}).execute()

            logging.info(res.data)

            kw_id = await get_id_for_keyword(client, keyword)

        res = (
            await client.from_("keyword_for_software")
            .insert({"software": software_id, "keyword": kw_id})
            .execute()
        )

        logging.info(res.data)


async def get_id_for_organisation(client, org):
    res = (
        await client.from_("organisation")
        .select("id", "name")
        .eq("name", org)
        .execute()
    )

    if len(res.data) > 0:
        return res.data[0].get("id")

    return None


async def organisation_has_logo(client, org) -> bool:
    org_id = await get_id_for_organisation(client, org)
    res = (
        await client.from_("organisation")
        .select("id", "logo_id")
        .eq("id", org_id)
        .execute()
    )
    if len(res.data) == 1 and res.data[0]['logo_id'] is not None:
        return True
    else:
        return False


async def add_organisations(client, spotlight):
    orgs = spotlight.get("hgf_centers")
    if isinstance(orgs, str):
        orgs = [orgs]

    if orgs is None or len(orgs) == 0:
        # no organisation specified
        return

    name = spotlight.get("name")
    slug = name_to_slug(name)
    software_id = await slug_to_id(client, slug)

    logging.info("Add organisations for %s", name)

    for org in orgs:
        org_id = await get_id_for_organisation(client, org)

        if org_id is None:
            logging.info("Adding organisation %s" % org)

            org_slug = org_name_to_slug(org)
            ror_id = "https://ror.org/%s" % ORGANISATIONS.get(org).get("ror") or None
            if ror_id is None or ror_id == "https://ror.org/":
                logging.warn("Could not find ROR Id for: %s" % org)

            res_img = (
                await client.from_("organisation")
                .insert({"name": org, "slug": org_slug, "ror_id": ror_id})
                .execute()
            )

            logging.info(res_img.data)

            org_id = await get_id_for_organisation(client, org)

        logo_exists = await organisation_has_logo(client, org)
        logo_available = (
            org in ORGANISATIONS.keys() and "logo" in ORGANISATIONS.get(org).keys()
        )
        if not logo_exists and not logo_available:
            logging.warn("No logo found for %s" % org)
            MISSING_LOGOS.append(org)
        elif not logo_exists:
            logo_filename = f"./resources/logos/{ORGANISATIONS[org]['logo']}"
            logging.info("Adding logo %s" % logo_filename)
            with open(logo_filename, "rb") as logo:
                logo_base64 = base64.b64encode(logo.read()).decode("utf-8")
                mime_type = mime.from_file(logo_filename)
                logo_data = {
                    "data": logo_base64,
                    "mime_type": mime_type,
                }
                res_img = (
                    await client.from_("image")
                    .insert(logo_data)
                    .execute()
                )
                logging.info(res_img.data)
                logo_id = res_img.data[0]['id']
                logging.info("Uploaded logo %s" % logo_filename)
            res_org = (
                await client.from_("organisation")
                .update({"logo_id": logo_id})
                .eq("id", org_id)
                .execute()
            )
            logging.info("Added logo %s to organisation %s" % {logo_id, org_id})
            logging.info(res_org.data)

        logging.info("Adding organisation %s to software %s" % (org, name))

        res_img = (
            await client.from_("software_for_organisation")
            .insert({"software": software_id, "organisation": org_id})
            .execute()
        )

        logging.info(res_img.data)


async def add_research_field(client, spotlight):
    research_field = spotlight.get("hgf_research_field")

    if research_field is None or len(research_field) == 0:
        # no research field specified
        return

    name = spotlight.get("name")
    slug = name_to_slug(name)
    software_id = await slug_to_id(client, slug)

    logging.info("Add research field for %s", name)

    kw_id = await get_id_for_keyword(client, research_field)

    if kw_id is None:
        logging.info("Adding research field %s" % research_field)

        res = await client.from_("keyword").insert({"value": research_field}).execute()

        logging.info(res.data)

        kw_id = await get_id_for_keyword(client, research_field)

    res = (
        await client.from_("keyword_for_software")
        .insert({"software": software_id, "keyword": kw_id})
        .execute()
    )

    logging.info(res.data)


async def process_imprint(client):
    filename = "./resources/Imprint.md"
    with open(filename, "r") as imprint:
        logging.info("Processing imprint from %s", filename)

        data = {
            "slug": "imprint",
            "title": "Imprint",
            "description": imprint.read(),
            "is_published": True,
            "position": 1,
        }

        db_imprint = (
            await client.from_("meta_pages").select("*").eq("slug", "imprint").execute()
        )

        if len(db_imprint.data) > 0 and not UPDATE_IMPRINT:
            logging.info("Imprint already exists, but will not be updated.")
            return
        elif len(db_imprint.data) > 0 and UPDATE_IMPRINT:
            logging.info("Imprint already exsits. Updating.")
            res = await client.from_("meta_pages").update(data).execute()
        else:
            logging.info("Imprint not found. Creating.")
            res = await client.from_("meta_pages").insert(data).execute()
        logging.info(res.data)


def check_env():
    errors = 0
    if not POSTGREST_URL:
        errors += 1
        logging.error("POSTGREST_URL undefined.")
    if not PGRST_JWT_SECRET:
        errors += 1
        logging.error("PGRST_JWT_SECRET undefined.")
    if errors > 0:
        raise RuntimeError("Environment variables are missing.")
    logging.info("Runtime variables checked.")


async def main():
    check_env()
    token = jwt.encode(JWT_PAYLOAD, PGRST_JWT_SECRET, algorithm=JWT_ALGORITHM)
    spotlights = get_spotlights()
    created_spotlights = []
    skipped_errors = []
    skipped_no_update = []

    async with AsyncPostgrestClient(POSTGREST_URL) as client:
        client.auth(token=token)
        await process_imprint(client)

        for spot in spotlights:
            # check if spotlight matches our criteria
            if len(spot.get("description", "")) > 10000:
                skipped_errors.append([spot.get("name"), "Description too long."])
                continue

            already_exists = await spotlight_exists(client, spot)
            if already_exists and DELETE_SPOTLIGHTS:
                # update existing -> remove first
                await remove_spotlight(client, spot)
            elif already_exists and not DELETE_SPOTLIGHTS:
                skipped_no_update.append(spot.get("name"))
                continue

            await add_spotlight(client, spot)
            await add_spotlight_urls(client, spot)
            await add_license(client, spot)
            await add_keywords(client, spot)
            await add_research_field(client, spot)
            await add_organisations(client, spot)
            created_spotlights.append(spot.get("name"))

    if len(created_spotlights) == 0:
        print("No new spotlights created.")
    else:
        print("The following spotlights were created:")
        for name in created_spotlights:
            print("  %s" % name)
    if len(skipped_no_update) > 0:
        print("The following spoltights already existed and were not updated:")
        for name in skipped_no_update:
            print("  %s" % name)
    if len(skipped_errors) > 0:
        print("The following spotlights were skipped because there were errors:")
        for name, reason in skipped_errors:
            print("  %s: %s" % (name, reason))
    if len(MISSING_LOGOS) > 0:
        print("There were logos missing of the following organisations:")
        for org in MISSING_LOGOS:
            print("  %s" % org)


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Migrate Software spotlights from hifis.net to the RSD.",
        usage="%(prog)s [OPTION]",
    )
    parser.add_argument(
        "-d",
        "--delete_all",
        action="store_true",
        help="Delete all spotlights and overwrite with current versions.",
    )
    parser.add_argument(
        "-i",
        "--update_imprint",
        action="store_true",
        help="Update imprint if it already exists.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase verbosity."
    )
    return parser


if __name__ == "__main__":
    mdparser = init_parser()
    args = mdparser.parse_args()
    DELETE_SPOTLIGHTS = args.delete_all
    UPDATE_IMPRINT = args.update_imprint
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARN)

    asyncio.run(main())

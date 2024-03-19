# Changelog

## [Unreleased](https://github.com/hifis-net/RSD-Spotlight-Migration/tree/HEAD)

[Full Changelog](https://github.com/hifis-net/RSD-Spotlight-Migration/compare/v1.5.1...HEAD)

**Closed issues:**

- Pass file path to spotlight directory at runtime [\#50](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/50)
- delete on table "release" violates foreign key constraint "release\_version\_release\_id\_fkey" on table "release\_version" [\#48](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/48)
- foreign key constraint "software\_highlight\_software\_fkey" violation [\#44](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/44)
- Extend slugify method [\#31](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/31)
- Removing a software entry without release / DOI not possible  [\#28](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/28)
- Nested lists in Markdown broken [\#27](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/27)

**Merged pull requests:**

- build\(deps-dev\): bump black from 23.11.0 to 24.3.0 [\#60](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/60) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps-dev\): bump isort from 5.12.0 to 5.13.2 [\#59](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/59) ([dependabot[bot]](https://github.com/apps/dependabot))
- Update GitHub actions workflows [\#58](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/58) ([Normo](https://github.com/Normo))
- Update dockerfile [\#52](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/52) ([Normo](https://github.com/Normo))
- feat: pass spotlights directory path as positional argument ... [\#51](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/51) ([Normo](https://github.com/Normo))
- Fix removal of release content [\#49](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/49) ([Normo](https://github.com/Normo))
- ci: add CI/CD workflow [\#47](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/47) ([Normo](https://github.com/Normo))
- chore: upgrade python to version 3.12 [\#46](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/46) ([Normo](https://github.com/Normo))
- fix: remove related software hihlights [\#45](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/45) ([Normo](https://github.com/Normo))
- build\(deps\): bump pyyaml from 6.0 to 6.0.1 [\#40](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/40) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps-dev\): bump black from 22.10.0 to 23.11.0 [\#39](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/39) ([dependabot[bot]](https://github.com/apps/dependabot))
- build\(deps\): bump actions/checkout from 3 to 4 [\#35](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/35) ([dependabot[bot]](https://github.com/apps/dependabot))
- Merge UFZ Develop branch [\#34](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/34) ([Normo](https://github.com/Normo))
- Code formatting [\#33](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/33) ([Normo](https://github.com/Normo))
- Stop removing newlines followed by a whitespace [\#30](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/30) ([Normo](https://github.com/Normo))
- Catch postgrest APIError when querying software releases [\#29](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/29) ([Normo](https://github.com/Normo))

## [v1.5.1](https://github.com/hifis-net/RSD-Spotlight-Migration/tree/v1.5.1) (2023-02-07)

[Full Changelog](https://github.com/hifis-net/RSD-Spotlight-Migration/compare/v1.5.0...v1.5.1)

**Merged pull requests:**

- Fix retrieval of org\_id [\#26](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/26) ([cmeessen](https://github.com/cmeessen))

## [v1.5.0](https://github.com/hifis-net/RSD-Spotlight-Migration/tree/v1.5.0) (2023-02-07)

[Full Changelog](https://github.com/hifis-net/RSD-Spotlight-Migration/compare/v1.4.0...v1.5.0)

**Closed issues:**

- Update image upload [\#23](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/23)
- Reduce Docker image size [\#20](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/20)

**Merged pull requests:**

- 20230207 update spotlights [\#25](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/25) ([cmeessen](https://github.com/cmeessen))
- 23 fix image upload [\#24](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/24) ([cmeessen](https://github.com/cmeessen))
- Replace gitlab.hzdr.de with codebase.helmholtz.cloud [\#22](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/22) ([Normo](https://github.com/Normo))

## [v1.4.0](https://github.com/hifis-net/RSD-Spotlight-Migration/tree/v1.4.0) (2022-10-28)

[Full Changelog](https://github.com/hifis-net/RSD-Spotlight-Migration/compare/v1.3.0...v1.4.0)

**Implemented enhancements:**

- Add RORs [\#18](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/18)
- Reduce Docker image size [\#21](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/21) ([cmeessen](https://github.com/cmeessen))

**Closed issues:**

- Add missing logos [\#15](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/15)

**Merged pull requests:**

- Adds ROR ids [\#19](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/19) ([cmeessen](https://github.com/cmeessen))
- Fix Organisation Logos [\#17](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/17) ([cmeessen](https://github.com/cmeessen))

## [v1.3.0](https://github.com/hifis-net/RSD-Spotlight-Migration/tree/v1.3.0) (2022-10-27)

[Full Changelog](https://github.com/hifis-net/RSD-Spotlight-Migration/compare/v1.2.1...v1.3.0)

**Closed issues:**

- Update HZDR name [\#16](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/16)
- Do not remove old spotlights [\#13](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/13)

**Merged pull requests:**

- Keep existing spotlights when migrating [\#14](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/14) ([cmeessen](https://github.com/cmeessen))
- Update to the latest hifis.net version [\#12](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/12) ([tobiashuste](https://github.com/tobiashuste))

## [v1.2.1](https://github.com/hifis-net/RSD-Spotlight-Migration/tree/v1.2.1) (2022-07-26)

[Full Changelog](https://github.com/hifis-net/RSD-Spotlight-Migration/compare/v1.2.0...v1.2.1)

**Closed issues:**

- Unwrap markdown text [\#5](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/5)

## [v1.2.0](https://github.com/hifis-net/RSD-Spotlight-Migration/tree/v1.2.0) (2022-07-26)

[Full Changelog](https://github.com/hifis-net/RSD-Spotlight-Migration/compare/v1.0.0...v1.2.0)

**Implemented enhancements:**

- Adds organisation logos [\#11](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/11) ([cmeessen](https://github.com/cmeessen))
- Build only on push to main [\#10](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/10) ([cmeessen](https://github.com/cmeessen))
- Adds imprint migration [\#9](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/9) ([cmeessen](https://github.com/cmeessen))

**Closed issues:**

- Build images only on push to main branch \(or tag\) [\#7](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/7)
- Add imprint [\#4](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/4)
- Add institution logos [\#3](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/3)

**Merged pull requests:**

- Update submodule [\#8](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/8) ([cmeessen](https://github.com/cmeessen))
- Remove line breaks in Markdown paragraphs [\#6](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/6) ([cmeessen](https://github.com/cmeessen))

## [v1.0.0](https://github.com/hifis-net/RSD-Spotlight-Migration/tree/v1.0.0) (2022-07-22)

[Full Changelog](https://github.com/hifis-net/RSD-Spotlight-Migration/compare/fbd5a633ea8401398eb0315447131d08e04b590a...v1.0.0)

**Closed issues:**

- Create an action that builds the RSD migration docker image [\#1](https://github.com/hifis-net/RSD-Spotlight-Migration/issues/1)

**Merged pull requests:**

- Add actions workflow to build and publish docker image [\#2](https://github.com/hifis-net/RSD-Spotlight-Migration/pull/2) ([Normo](https://github.com/Normo))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*

<!-- file generated with AI assistance: Claude Code - 2026-07-01 17:10:01 UTC -->

# dmstr/symfony-recipes

Public [Symfony Flex](https://github.com/symfony/flex) recipe endpoint for
`dmstr/*` packages that need more than a plain bundle registration — e.g. an
accompanying Docker service.

## Available recipes

| Package | Provides |
|---|---|
| [`dmstr/flowable-bundle`](https://github.com/dmstr/flowable-bundle) | registers `Dmstr\Flowable\FlowableBundle` and ships `docker/docker-compose.flowable.yml` (Flowable REST engine + PostgreSQL) |

## Consumer configuration

Add this endpoint to the app's `composer.json` (before `flex://defaults`):

```json
{
    "extra": {
        "symfony": {
            "endpoint": [
                "https://raw.githubusercontent.com/dmstr/symfony-recipes/flex/main/index.json",
                "flex://defaults"
            ]
        }
    }
}
```

`composer require dmstr/flowable-bundle` then applies the recipe: the bundle is
registered and the Docker compose fragment is copied into `docker/`. The
fragment is named `docker/docker-compose.flowable.yml` so a Makefile
`COMPOSE_FILE` glob (`docker/docker-compose.*.yml`) picks it up automatically —
the service is only present in projects that install the bundle, never baked
into a skeleton.

## Layout

```
<vendor>/
└── <package>/
    └── <version>/
        ├── manifest.json                 ← bundles + copy-from-recipe + env
        └── docker/…                      ← files rolled into the app
index.json                                ← lists available recipes for Flex
<vendor>.<package>.<version>.json         ← generated flattened recipe (base64 files)
```

## Updating

After adding or editing a recipe under `<vendor>/<package>/<version>/`, run:

```bash
python3 bin/build-recipes.py
```

This regenerates the flattened `<vendor>.<package>.<version>.json` files (Flex
base64-decodes file contents) and the `recipes` map in `index.json`. Commit the
generated files.

## License

[MIT](https://opensource.org/licenses/MIT) © diemeisterei GmbH

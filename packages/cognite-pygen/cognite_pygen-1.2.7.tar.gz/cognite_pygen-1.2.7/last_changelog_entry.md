
### Fixed

- When generating an SDK with views that overwrites parent properties,
`pygen` now includes the overwritten field in the child classes. For
example, if you have a `Batch` view that implements `CogniteActivity`
and overwrites the `assets` property to be of value type `MyAsset`,
`pygen` will now retrieve `MyAsset`s instead of `CogniteAsset`.
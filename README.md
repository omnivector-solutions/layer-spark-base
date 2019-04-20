# layer-spark-base

Use this layer to provide the spark tarball, user, perms, and initial base config.

### Usage
To use this layer, add `lasyer:spark-base` to you layer.yaml.
```yaml
includes:
- 'layer:spark-base'
```

### Flags
- `'spark.base.available'`

The `'spark.base.available'` flag will become set and available
for your reactive layer to gate against when the provisioning of spark
is complete.

##### License
- GPLv3 (see `LICENSE` file in this directory)

##### Copyright
- Omnivector Solutions &copy; 2018 <admin@omnivector.solutions>

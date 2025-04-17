# configs.py: last updated 09:35 AM on April 17, 2025

**File Path:** `WIP/test_generator/configs.py`

## Table of Contents

### Classes

- [`Configs`](#configs)

## Classes

## `Configs`

```python
class Configs(BaseModel)
```

Configuration settings for test generator.

Validates and stores command-line arguments and settings.

**Methods:**

- [`validate_harness`](#validate_harness)

### `validate_harness`

```python
def validate_harness(self, cls, v)
```

Validate test harness name.

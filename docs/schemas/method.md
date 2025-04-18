# method.py: last updated 11:35 PM on April 17, 2025

**File Path:** `WIP/test_generator/schemas/method.py`

## Table of Contents

### Classes

- [`Method`](#method)

## Classes

## `Method`

```python
class Method(BaseModel)
```

Describes the method used for testing.

**Methods:**

- [`comments`](#comments) (property)

### `comments`

```python
def comments(self)
```

Generate comments for the test method.

**Returns:**

- `str`: Formatted test method comments with each step on its own line

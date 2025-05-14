# crudtape

> _"Like duck tape but for CRUD..."_

A lightweight in-memory [CRUD](https://developer.mozilla.org/en-US/docs/Glossary/CRUD) store for Pydantic-style objects, designed for rapid prototyping. Powered by [TinyDB](https://tinydb.readthedocs.io/en/latest/index.html).

## Installation

```shell
pip install crudtape
```

## Usage

The store is designed to work with any model class that implements the basic `Storable` [protocol](./src/crudtape/store.py#L13), which defines a minimal subset of the Pydantic [model](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel/) interface.
Importantly, the store does not depend on Pydantic itself - you can use any compatible class. This means:

- Pydantic models (as-is)
- `@dataclass` decorated classes 
- Custom classes built from scratch

The only caveat is that the store manages the object IDs internally. In essence, a compatible model class needs to provide:

- `__init__` method that accepts keyword arguments, including an optional id of type int (used when constructing returned objects).
- `model_dump()` method returning a dictionary representation, excluding the `id` attribute (it will be ignored by the store otherwise).

```python
import BaseModel from pydantic

class Pet(BaseModel):
    name: str
    age: str
    id: int = None
```        

Additional examples are shown in the [test suit](./tests/crudtape/test_utils.py).

The class is used to create a corresponding store instance:

```python
import Store from crudtape

store = Store(Pet)
```

The store offers basic self-explanatory CRUD operations, all typed to the specified model class and with decent error checking. See the [API reference](https://alesbukovsky.github.io/crudtape/) for full details.

```python
# insert an object
store.insert(Pet(name="Bob", age=3))

# list all objects 
store.all()

# get an object with given ID
store.get(1)

# update an object with given ID
store.update(1, Pet(name="Rob", age=5))

# delete an object with given ID
store.delete(1)
```

The store raises `StoreError` for general failures, with two exceptions: `NotFoundError` is raised when an object with the given ID doesn’t exist, and `TypeError` when an input object has the wrong type.
 
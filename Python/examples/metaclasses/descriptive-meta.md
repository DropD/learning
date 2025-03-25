---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.2
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
import dataclasses
import types
import fractions
```

```python
def make_fluid_setter(attr_name):
    def fluid_setter(self, value):
        getattr(self, f"validate_{attr_name}_change", lambda: None)()
        return self.__class__(**(self.as_dict() | {attr_name: value}))
    return fluid_setter


class Missing:
    pass


class FluidMeta(type):
    @classmethod
    def __new__(cls, meta, name, bases, namespace):
        buildee = namespace["__annotations__"]["buildee"]
        builder_attrs = {}
        if dataclasses.is_dataclass(buildee):
            fields = dataclasses.fields(buildee)
            builder_attrs |= {field.name: field.default for field in fields}
        builder_attrs |= {attr: value for attr, value in namespace.items() if not attr.startswith("_") and not isinstance(value, types.FunctionType)}
        namespace["__builder_attrs"] = list(builder_attrs.keys())
        
        def as_dict(self):
            return {attr: getattr(self, f"__{attr}") for attr in getattr(self, "__builder_attrs")}
        namespace["as_dict"] = as_dict

        def init(self, **kwargs):
            for attr, value in kwargs.items():
                setattr(self, f"__{attr}", value)
        namespace["__init__"] = init
            
        for attr, default_value in builder_attrs.items():
            private_name = f"__{attr}"
            namespace[private_name] = default_value
            namespace[attr] = make_fluid_setter(attr)

        def build(self):
            getattr(self, "validate", lambda: None)()
            data = {k: v for k, v in self.as_dict().items() if not isinstance(v, dataclasses._MISSING_TYPE)}
            return buildee(**data)
        namespace["build"] = build
            
        return super().__new__(meta, name, bases, namespace)
```

```python
@dataclasses.dataclass(frozen=True)
class Rectangle:
    height: int
    width: int
    color: str = "no_color"
    border_color: str = "black"


class FluidRectangleBuilder(metaclass=FluidMeta):
    buildee: Rectangle
    height: int = 1
    width: int = 1
    

class ThreeFourthsBuilder(metaclass=FluidMeta):
    buildee: Rectangle
    height: int = 1
    width: int = 1
    border_color: str = "blue"

    def validate(self) -> None:
        data = self.as_dict()
        if (ratio := fractions.Fraction(data["height"], data["width"])) != fractions.Fraction(3, 4):
            raise ValueError(f"ThreeFourthsRectangle can not be built with width / height ratio of {ratio}.")
```

```python
f = FluidRectangleBuilder()
```

```python
f.border_color("blue").color("white").height(3).build()
```

```python
ThreeFourthsBuilder(height=9, width=16).build()
```

```python
ThreeFourthsBuilder(height=6, width=8).build()
```

```python
import textwrap


def ask_chat_gpt(name: str, description: str) -> str:
    ## TODO: send a https request to ChatGPT asking something like
    ## "Please implement a class with name <name> in Python, which behaves as described
    ## in the following docstring: <description>"
    ## 
    ## for now just return a placeholder
    return textwrap.dedent(f'''
    class {name}:
        """{description}"""

        def __call__(self) -> str:
            return "Sorry, I was too lazy to actually ask ChatGPT."
    ''')


class GptMeta(type):
    @classmethod
    def __new__(cls, meta, name, bases, namespace):
        code = ask_chat_gpt(name=name, description=namespace["__doc__"])
        exec(code)
        return locals()[name]


class SomeClass(metaclass=GptMeta):
    """Describe here how the class should behave."""
```

```python
SomeClass()()
```

```python
from __future__ import annotations


@dataclasses.dataclass
class FloatScalar:
    unit: Unit
    value: float

    def __sub__(self, other: FloatScalar) -> FloatScalar:
        if other.unit != self.unit:
            raise ValueError("Units do not match.")
        return FloatScalar(unit=self.unit, value=self.value - other.value)


@dataclasses.dataclass
class Unit:
    name: str
    
    def __rmul__(self, value: float) -> FloatScalar:
        return FloatScalar(unit=self, value=value)


UNIT_Da = UNIT_u = Unit("Dalton")


class He:
    __mass: static[const[[float]]] = 4.0026 * UNIT_u

    @property
    def mass(self):
        return self.__class__.__mass

    
    # def __setitem__(self, name, value):
    #     if "__mass" in name:
    #         raise NotImplemented("Can not change the mass this way")
    

particles = [He(), He(), He()]

#}particles[0].mass = 4 * UNIT_u

assert numpy.allclose(numpy.array([(p.mass - 4.0026 * UNIT_u).value for p in particles]), 0)
```

```python
particles[0].mass
```

```python
def mass_changer(cls, value):
    keys = cls.__dict__
    mass_key = [k for k in keys if "__mass" in k][0]
    setattr(cls, mass_key, value)

He.change_mass = classmethod(mass_changer)
```

```python
He.change_mass(5 * UNIT_u)
```

```python
particles[0].mass
```

```python
He().mass
```

```python
He.__dict__
```

```python

```

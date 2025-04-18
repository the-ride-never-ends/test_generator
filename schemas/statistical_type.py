import enum


class StatisticalType(enum.StrEnum):
    """
    An enumeration that defines the statistical types of variables.
    The statistical types are:
    - NOMINAL: A nominal variable is one that describes a name, label or category without natural order.
    - ORDINAL: An ordinal variable is a variable whose values are defined by an order relation between the different categories.
    - CONTINUOUS: A continuous variable can assume an infinite number of real values within a given interval.
    - DISCRETE: A discrete variable can assume only a finite number of real values within a given interval.
    """
    NOMINAL = "nominal"
    ORDINAL = "ordinal"
    CONTINUOUS = "continuous"
    DISCRETE = "discrete"

import math

registry = {}


def register(cls):
    registry[cls.__name__] = cls()


class MetaCalculation(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        # Validate
        print(class_dict['__call__'])
        if not class_dict.get('__call__'):
            raise ValueError('All calculation classes need to implement __call__! >:(')
        if not class_dict.get('__call__').__code__.co_argcount == 2:
            print(class_dict.get('__call__').__code__.co_argcount)
            raise ValueError('All calculation classes should take one param in addition to self, a list of values! >8(')
        # Register
        register(cls)
        return cls


class Add(metaclass=MetaCalculation):
    def __call__(self, values):
        return sum(values)


class Subtract(metaclass=MetaCalculation):
    def __call__(self, values):
        return values[0] - sum(values[1:])


class Multiply(metaclass=MetaCalculation):
    def __call__(self, values):
        return math.prod(values)


class Divide(metaclass=MetaCalculation):
    def __call__(self, values):
        result = 0
        for i in values:
            result = result / values[i]
        return result


def calculator(val):
    choice = input('[B]egin calculation, [q]uit or [c]ontinue with ' + str(float(val)) + '?     ').lower()
    if choice == 'q':
        return

    values = input('Enter values as comma-separated list:       ')
    values = [float(val) for val in values.split(',')]

    if choice == 'c':
        values.insert(0, val)

    operation = input(', '.join([f'[{operation[0]}]: {operation}' for operation in registry.keys()]) + ':   ')
    operation_calculation = [key for key in registry.keys() if key[0] == operation]
    if not operation_calculation:
        print('Operation not found: ', operation)
    result = registry.get(operation_calculation[0])(values)
    print(result)
    calculator(result)


calculator(0)

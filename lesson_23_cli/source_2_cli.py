import argparse
from enum import Enum

parser = argparse.ArgumentParser()

class Environment(Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


parser.add_argument(
    "name",
    )
# parser.add_argument(
#     "salary",
#     )
parser.add_argument(
    "--host",
    required=True
    # default="localhost"
)
parser.add_argument(
    "-a",
    "--age",
    type=int
)
parser.add_argument(
    "--env",
    choices=[e.value for e in Environment]
)


args = parser.parse_args()

print(f"Hello, {args.name}")
print(f"age, {args.age}, {type(args.age)}")
print([e for e in Environment])

username = "superadmin"
password = "$3kDFfj!@2"

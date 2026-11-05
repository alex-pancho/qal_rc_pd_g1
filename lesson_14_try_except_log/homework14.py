def sum_numbers_in_list(string_list: list):
    """Повертає список сум чисел зі списку строк,
    які складаються з чисел, розділених комою."""

    if not isinstance(string_list, list) or len(string_list) == 0:
        raise ValueError("Некоректні вхідні дані")

    result = []

    for item in string_list:
        try:
            numbers = item.split(",")
            total = 0

            for number in numbers:
                total += int(number)

            result.append(total)

        except ValueError:
            result.append("Не можу це зробити!")

        except AttributeError:
            result.append("Не можу це зробити! AttributeError")

    return result


if __name__ == "__main__":
    output = sum_numbers_in_list(["1,2,3", "4,0,6"])
    print(output)

    output = sum_numbers_in_list(["1,2,3", "asas7,8,9", "4,0,6"])
    print(output)

    output = sum_numbers_in_list(["1,2,3,4", 7])
    print(output)
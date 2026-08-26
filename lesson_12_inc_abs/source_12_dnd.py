class Money:

    def __init__(self, amount: float) -> None:
        self.__amount = amount

    def __str__(self):
        return f"{self.__amount:.2f}"

    def __add__(self, other):
        if not isinstance(other, (float, int, Money)):
            raise TypeError(f"int or float expected, {type(other)} got")
        if isinstance(other, Money) and type(self) == type(other):
            # return Money(self.__amount + other._Money__amount)
            return Money(self.__amount + other.amount)
        elif isinstance(other, (float, int)):
            self.__amount = self.__amount + other
            return self.__amount
        else:
            raise TypeError (f"{type(self)} != {type(other)}, only equal type is supported")
        
    def __sub__(self, other):
        if not isinstance(other, Money):
            raise TypeError(f"int or float expected, {type(other)} got")
        if isinstance(other, Money) and type(self) == type(other):
            return Money(self.__amount - other.amount) # _Money__amount
        # else:
        #     return Money(self.__amount - other)
    
    @property
    def amount(self):
        return self.__amount


class UAH(Money):

    def __init__(self, amount: float) -> None:
        Money.__init__(self, amount)
        # super().__init__(amount)

    def __str__(self):
        return f"{self.amount:.2f} грн"


class USD(Money):

    def __init__(self, amount: float) -> None:
        Money.__init__(self, amount)
        # super().__init__(amount)

    def __str__(self):
        return f"${self.amount:.2f}"


class ForEx():
    def __init__(self, exchange_rate_bye, exchange_rate_sell):
        self.__exchange_rate_bye = exchange_rate_bye
        self.__exchange_rate_sell = exchange_rate_sell

    @property
    def exchange_rate_bye(self):
        return self.__exchange_rate_bye
    
    @exchange_rate_bye.setter
    def exchange_rate_bye(self, value:int):
        if value > self.__exchange_rate_sell:
            self.__exchange_rate_bye = value
    
    @property
    def exchange_rate_sell(self):
        return self.__exchange_rate_sell

    @exchange_rate_sell.setter
    def exchange_rate_sell(self, value:int):
        if value < self.__exchange_rate_bye:
            self.__exchange_rate_sell = value

    def convert(self, cur_amount):
        if isinstance(cur_amount, UAH):
            usd_amount = cur_amount.amount / self.__exchange_rate_sell
            return USD(usd_amount)
        if isinstance(cur_amount, USD):
            uah_amount = cur_amount.amount * self.__exchange_rate_bye
            return UAH(uah_amount)
        else:
            raise TypeError("Wrong type for convert: UAH USD is supported")


if __name__ == "__main__":
    my_first_money = Money(102.33)
    print(my_first_money)
    my_sec_money = Money(42.57)
    a = my_first_money + my_sec_money
    print(a)
    b = a + 3
    print(b)

    my_uah_cash = UAH(3000)
    my_wife_uah = UAH(2000)
    my_fam_money = my_uah_cash + my_wife_uah
    print(my_fam_money)
    my_usd_cash = USD(100)
    my_wife_usd = USD(2000)
    my_fam_money_usd = my_usd_cash + my_wife_usd
    print(my_fam_money_usd)

    privatbank = ForEx(43.05, 43.57)
    akord_bank = ForEx(44.27, 44.90)

    pb_to_uah = privatbank.convert(my_usd_cash)
    pb_to_usd = privatbank.convert(my_uah_cash)
    ak_to_uah = akord_bank.convert(my_usd_cash)
    ak_to_usd = akord_bank.convert(my_uah_cash)

    print(f"Продати {my_usd_cash}:", pb_to_uah, "|", ak_to_uah)
    print(f"Купити на {my_uah_cash}:", pb_to_usd, "|", ak_to_usd)


"""
    object.__add__(self, other) +
    object.__sub__(self, other) -
    object.__mul__(self, other) *
    object.__matmul__(self, other)  -------
    object.__truediv__(self, other) /
    object.__floordiv__(self, other) //
    object.__mod__(self, other) %
    object.__divmod__(self, other) 
    object.__pow__(self, other[, modulo]) **
    object.__lshift__(self, other) >>
    object.__rshift__(self, other) <<
    object.__and__(self, other) &
    object.__xor__(self, other)  -------
    object.__or__(self, other) |
"""
print(5 / 3)
print(5 // 3)
print(5 % 3)



class Person():
    __age = 0

    def __init__(self, age:int = 0) -> None:
        self.age = age

    @property
    def age(self):
        return f"{self.__age} years old"
    
    @age.setter
    def age(self, years: int):
        if not isinstance(years, int):
            raise ValueError("add_year must be int")
        if years >= self.__age:
            self.__age = years
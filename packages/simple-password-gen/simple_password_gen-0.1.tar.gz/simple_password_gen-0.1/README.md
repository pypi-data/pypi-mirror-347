# simple_password

این یک کتابخانه‌ی ساده برای ساخت پسورد تصادفی در پایتون است.

## نحوه استفاده

```python
from simple_password import generate_password

password = generate_password(length=12, use_uppercase=True, use_digits=True, use_symbols=True)
print(password)
```

## پارامترها

- `length`: طول پسورد (پیش‌فرض ۱۲)
- `use_uppercase`: استفاده از حروف بزرگ (پیش‌فرض True)
- `use_digits`: استفاده از عدد (پیش‌فرض True)
- `use_symbols`: استفاده از نمادها مثل @#% (پیش‌فرض True)

from services.primes.usecases.check_primality import CheckPrimalityUseCase


def test_prime_number_is_true():
    assert CheckPrimalityUseCase().execute(7) is True


def test_one_and_zero_are_not_prime():
    uc = CheckPrimalityUseCase()
    assert uc.execute(1) is False
    assert uc.execute(0) is False


def test_large_composite_is_false():
    # 221 = 13 * 17
    assert CheckPrimalityUseCase().execute(221) is False


def test_negative_numbers_are_not_prime():
    assert CheckPrimalityUseCase().execute(-11) is False
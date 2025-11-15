from services.api_gateway.ports.prime_check import PrimeCheckPort


class CheckPrimalityProxyUseCase:
    def __init__(self, port: PrimeCheckPort):
        self.port = port

    def execute(self, n: int) -> bool:
        if not isinstance(n, int):
            raise ValueError("n must be int")
        return self.port.is_prime(n)
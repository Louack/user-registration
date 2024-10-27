from src.auth.adapters.services.dummy_email_service import DummyEmailService


class TestDummyEmailService:
    def test_send_activation_code(self, capsys):
        email_service = DummyEmailService()
        email = "test@test.com"
        code = "activation_code"

        email_service.send_activation_code(email, code)
        output = capsys.readouterr().out

        assert output == f"Activation code '{code}' sent to {email}...\n"

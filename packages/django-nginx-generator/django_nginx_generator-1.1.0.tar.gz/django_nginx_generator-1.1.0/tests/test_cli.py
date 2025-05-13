import subprocess
import sys

def test_help():
    result = subprocess.run(
        [sys.executable, "-m", "django_nginx_generator.cli", "--help"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Usage" in result.stdout or "usage" in result.stdout

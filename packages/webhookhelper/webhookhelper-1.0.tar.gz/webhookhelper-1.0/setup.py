from setuptools import setup

version = "1.0"

setup(
    name="webhookhelper",
    version=version,
    description="A simple webhook helper for Discord and Telegram",
    author="NotOfficial",
    author_email="root@notoff.pro",
    keywords="webhook discord telegram",
    include_package_data=True,
    zip_safe=False,
    packages=["WebhookHelper"],
    package_dir={"WebhookHelper": "WebhookHelper"},
    download_url=f"https://github.com/NotOfficals/WebHookHelper/archive/refs/tags/{version}.zip",
    license="Apache License. Version 2.0, see LICENSE file",
    install_requires=["requests", "aiohttp", "urllib3"],
    python_requires=">=3.7",
)

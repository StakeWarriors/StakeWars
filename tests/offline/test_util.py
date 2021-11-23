from dotenv import load_dotenv
from scripts.deployments.new_deploy import (
    deploy_admin,
    deploy_swcu,
    deploy_swcu_proxy,
    deploy_swfu,
    deploy_swfu_proxy,
)
from scripts.deployments.new_mocks import deploy_link, deploy_vrfc


load_dotenv()
TOKENS_TO_MINT = 1
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
FAKE_ADDRESS = "0x0000000000000000000000000000000000000001"


def setup_prep():
    link_token_mock = deploy_link()
    proxy_admin = deploy_admin()
    swfactory = deploy_swfu()
    vrf_coordinator_mock = deploy_vrfc(link_token_mock)
    (proxy, proxy_admin, proxy_stakewars_factory) = deploy_swfu_proxy(
        10, swfactory, proxy_admin, vrf_coordinator_mock
    )
    stakewars_character = deploy_swcu()
    (proxy, proxy_admin, proxy_stakewars_character) = deploy_swcu_proxy(
        stakewars_character, proxy_admin
    )

    vrf_coordinator_mock.callBackWithRandomness(0, 1, proxy_stakewars_factory)
    return (proxy_stakewars_factory, proxy_stakewars_character)

class Settings:
    """ A class to store all configuration settings for ISP Switcher script """

    def __init__(self):
        # Check Point management server settings
        self.mgmt_username = "test_user"  # checkpoint webapi user
        self.mgmt_password = "vpn123"  # checkpoint webapi user password
        self.mgmt_server = "192.168.1.1"  # ip address of the checkpoint mgmt server with webapi enabled
        self.mgmt_port = 443  # port number of the checkpoint management server
        self.target_gws = [
            "CP8030TestNode1",
            "CP8030TestNode2",
        ]  # target gw or gws with ISP redundancy activated (in case of cluster use [gw1_name,gw2_name])

        # Internet Service Provider Settings
        self.isp1_name = "ISP_1"  # name of ISP 1 in ISP redundancy settings
        self.isp2_name = "ISP_2"  # Name of ISP 2 in ISP redundancy settings
        self.isp1_desc = "Internet Service Provider 1"  # full name of ISP 1
        self.isp2_desc = "Internet Service Provider 2"  # full name of ISP 2

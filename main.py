import matplotlib.pyplot as plt
from prettytable import PrettyTable


class NetworkCalculator:
    def __init__(self, mask: int, ip: str):
        self.mask = mask
        self.ip = ip

    @staticmethod
    def dec_representation(binary_rep: list[int]) -> str:
        res = ''
        pow_index = 7
        temp = 0
        for i in binary_rep:
            if pow_index == 0:
                if i == 1:
                    temp += 1
                res += str(temp)
                res += '.'
                temp = 0
                pow_index = 7
                continue
            if i == 1:
                temp += 2**pow_index
            pow_index -= 1

        return res[:len(res)-1]

    @staticmethod
    def binary_representation(num: int) -> list[int]:
        # 8 bytes representation
        res = [0] * 8
        idx = 7
        while num > 0:
            if num % 2 == 0:
                res[idx] = 0
            else:
                res[idx] = 1
            num = num//2
            idx -= 1
        return res

    def change_address_into_binary(self) -> list[int]:
        splited_ip: list[str] = self.ip.split('.')
        binary_res: list[int] = []

        for num in splited_ip:
            num_in_binary = self.binary_representation(int(num))
            # Pad the binary representation with leading zeros to ensure 8 bits
            num_in_binary = [0] * (8 - len(num_in_binary)) + num_in_binary
            binary_res.extend(num_in_binary)

        return binary_res

    def change_mask_into_binary(self) -> list[int]:
        binary_mask: list[int] = [0] * 32

        for i in range(self.mask):
            binary_mask[i] = 1

        return binary_mask

    def calculate_network_address(self) -> list[int]:
        ip_binary_address: list[int] = self.change_address_into_binary()
        starting_byte: int = self.mask

        for i in range(32-self.mask):
            ip_binary_address[starting_byte] = 0
            starting_byte += 1

        return ip_binary_address

    def calculate_broadcast_address(self) -> list[int]:
        network_address = self.calculate_network_address()
        starting_byte: int = self.mask

        for i in range(32-self.mask):
            network_address[starting_byte] = 1
            starting_byte += 1
        return network_address

    def calculate_hosts_number(self):
        return 2**(32 - self.mask)-2

    def calculate_min_host_address(self) -> list[int]:
        network_address: list[int] = self.calculate_network_address()
        network_address[-1] = 1
        first_usable_host_address: list[int] = network_address
        return first_usable_host_address

    def calculate_max_host_address(self):
        broadcast_address: list[int] = self.calculate_broadcast_address()
        broadcast_address[-1] = 0
        last_usable_host_address: list[int] = broadcast_address
        return last_usable_host_address

    def display_data(self):
        network_address = self.calculate_network_address()
        broadcast_address = self.calculate_broadcast_address()
        last_usable_address = self.calculate_max_host_address()
        first_usable_address = self.calculate_min_host_address()

        # Create a PrettyTable
        table = PrettyTable()
        table.field_names = ["Property", "Value"]

        # Add rows to the table
        table.add_row(["IP", f"{self.ip}/{self.mask}"])
        table.add_row(
            ["Network Address", self.dec_representation(network_address)])
        table.add_row(
            ["Broadcast Address", self.dec_representation(broadcast_address)])
        table.add_row(
            ["Host Min", self.dec_representation(first_usable_address)])
        table.add_row(
            ["Host Max", self.dec_representation(last_usable_address)])
        table.add_row(["Hosts Number", str(self.calculate_hosts_number())])

        print(table)


n_object = NetworkCalculator(14, '10.10.13.112')
n_object.display_data()

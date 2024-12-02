class CommandBudget:
    def __init__(self):
        """
        Inisialisasi CommandBudget dengan daftar perintah untuk mengelola data anggaran.
        """
        self.commands = {
            "1": "Tambah Anggaran",
            "2": "Edit Anggaran",
            "3": "Hapus Anggaran",
            "4": "Tampilkan Semua Anggaran",
            "5": "Keluar"
        }

    def display_command(self):
        """
        Menampilkan daftar perintah yang dapat dilakukan user.
        """
        print("=== Command Budget ===")
        print("Pilih salah satu perintah berikut untuk mengelola data anggaran:")
        for key, command in self.commands.items():
            print(f"{key}. {command}")
        print("=======================")
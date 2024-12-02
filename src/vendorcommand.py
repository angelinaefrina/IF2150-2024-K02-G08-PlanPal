class VendorCommand:
    def display_command(self):
        """
        Menampilkan perintah-perintah yang dapat dilakukan user untuk mengelola data vendor.
        """
        print("\n=== Vendor Management Commands ===")
        print("1. Tambah Vendor")
        print("2. Lihat Daftar Vendor Berdasarkan EventID")
        print("3. Hapus Vendor Berdasarkan Nama dan EventID")
        print("4. Keluar dari Pengelolaan Vendor")
        print("\nMasukkan nomor perintah yang ingin dijalankan.")
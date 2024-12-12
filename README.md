# PlanPal
Sebuah aplikasi event planner untuk memudahkan mengelola acara

## Daftar Isi
- [Deskripsi Singkat](#deskripsi-singkat)
- [Cara Menjalankan Aplikasi](#cara-menjalankan-aplikasi)
- [Daftar Modul](#daftar-modul)
- [Daftar Tabel Basisdata](#daftar-tabel-basisdata)

## Deskripsi Singkat

## Cara Menjalankan Aplikasi

## Daftar Modul

### Modul X
### Modul X
### Pembagian Tugas

## Daftar Tabel Basisdata

1. [Tabel dan Atribut](#tabel-dan-atribut)
    - [Tabel 1: Event](#tabel-1-event)
    - [Tabel 2: Guest List](#tabel-2-guest-list)
    - [Tabel 3: Budget](#tabel-3-budget)
    - [Tabel 4: Vendor](#tabel-4-vendor)
    - [Tabel 5: Rundown](#tabel-5-rundown)

## Tabel dan Atribut

### Tabel 1: Event

Tabel ini berisi data event

| Atribut       | Tipe Data | Keterangan |
|---------------|-----------|------------|
| EventID       | Integer   |            |
| EventLocation | String    |            |
| EventDate     | Date      |            |
| EventStatus   | String    |            |

### Tabel 2: Guest List

Tabel ini berisi data tamu

| Atribut    | Tipe Data | Keterangan |
|------------|-----------|------------|
| EventID    | Integer   |            |
| GuestID    | Integer   |            |
| GuestName  | String    |            |
| RSVPStatus | String    |            |

### Tabel 3: Budget

Tabel ini berisi data budget

| Atribut             | Tipe Data | Keterangan |
|---------------------|-----------|------------|
| EventID             | Integer   |            |
| RequirementName     | String    |            |
| RequirementBudget   | Long      |            |
| RequirementQuantity | Long      |            |

### Tabel 4: Vendor

Tabel ini berisi data vendor

| Atribut       | Tipe Data | Keterangan |
|---------------|-----------|------------|
| EventID       | Integer   |            |
| VendorName    | String    |            |
| VendorContact | String    |            |
| VendorProduct | String    |            |

### Tabel 5: Rundown

Tabel ini berisi data rundown

| Atribut       | Tipe Data | Keterangan |
|---------------|-----------|------------|
| EventID       | Integer   |            |
| VendorName    | String    |            |
| VendorContact | String    |            |
| VendorProduct | String    |            |
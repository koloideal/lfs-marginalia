# my-lfs

LFS 13.1-systemd для ThinkPad X200s. Собирается в raw-образе диска на хосте Arch Linux, проверяется в QEMU (`-cpu Penryn`), заливается на ноутбук через `dd`/`zstd`.

## Структура

- `bin/lfs-chroot` — вход в chroot образа: подключает `lfs.img` через loop, монтирует виртуальные ФС и открывает shell; при выходе снимает то, что смонтировал сам
- `patches/fbcon-logo-right.patch` — `fbcon=logo-pos:right` для boot-логотипа (правый верхний угол, по аналогии с `center`)

## Флоу

```
lfs-chroot → правки/сборка внутри → exit → QEMU (snapshot=on) → zstd | ssh | dd на ноут
```

TODO: скрипты сборки образа, конфиги (fstab, grub.cfg, kernel .config), BLFS-порядок.

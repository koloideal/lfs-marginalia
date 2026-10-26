#!/usr/bin/env bash
# Подменяет логотип ядра logo_linux_clut224.ppm своим PPM-файлом.
# Запускать из chroot LFS. Использование:
#   ./apply.sh [путь/к/исходникам/ядра] [свой-logo.ppm]
set -euo pipefail

MOD_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SRC=${1:-.}
LOGO=${2:-$MOD_DIR/kolo-lfs-kernel-logo.ppm}
TARGET=drivers/video/logo/logo_linux_clut224.ppm

cd "$SRC"
[[ -f Makefile && -d drivers/video/logo ]] || {
  echo "ошибка: $SRC не похоже на корень исходников ядра" >&2
  exit 1
}
[[ -f $LOGO ]] || { echo "ошибка: нет файла логотипа: $LOGO" >&2; exit 1; }

if [[ ! -f $TARGET.orig ]]; then
  cp "$TARGET" "$TARGET.orig"
  echo "оригинал сохранён в $TARGET.orig"
else
  echo "$TARGET.orig уже существует — бэкап не изменяется"
fi

cp "$LOGO" "$TARGET"

if [[ -f .config ]]; then
  for opt in CONFIG_LOGO CONFIG_LOGO_LINUX_CLUT224; do
    grep -q "^$opt=y" .config ||
      echo "предупреждение: $opt не включён в .config" >&2
  done
fi

echo "готово: логотип подменён, можно собирать ядро"

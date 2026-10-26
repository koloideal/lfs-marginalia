#!/usr/bin/env bash
# Применяет fbcon-logo-right.patch к дереву исходников ядра.
# Запускать из chroot LFS. Использование:
#   ./apply.sh [путь/к/исходникам/ядра]     (по умолчанию — текущая директория)
set -euo pipefail

MOD_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SRC=${1:-.}

cd "$SRC"
[[ -f Makefile && -d drivers/video/fbdev ]] || {
  echo "ошибка: $SRC не похоже на корень исходников ядра" >&2
  exit 1
}

kver=$(make -s kernelversion 2>/dev/null || true)
if [[ -z $kver ]]; then
  echo "предупреждение: версию ядра определить не удалось" >&2
elif [[ $kver != 7.* ]]; then
  echo "предупреждение: патч проверялся на 7.2.x, обнаружена версия $kver — dry-run покажет, применим ли он" >&2
else
  echo "ядро $kver"
fi

patch -Np1 --dry-run -i "$MOD_DIR/fbcon-logo-right.patch" || {
  echo "сухая проверка не прошла — патч НЕ применялся" >&2
  exit 1
}
patch -Np1 -i "$MOD_DIR/fbcon-logo-right.patch"

if [[ -f .config ]]; then
  grep -q '^CONFIG_LOGO=y' .config ||
    echo "предупреждение: CONFIG_LOGO не включён — без него параметр ни на что не влияет" >&2
fi

echo "готово. соберите ядро и добавьте в cmdline: fbcon=logo-pos:right"

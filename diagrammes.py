import matplotlib.pyplot as plt
import re

# Étape 1 : Extraire les données depuis le texte brut
def parse_results(raw_text):
    data = {}
    current_file = ""
    memory_size = 0

    for line in raw_text.splitlines():
        if "Testing file" in line:
            match = re.search(r"Testing file: (\S+) with memory size: (\d+)", line)
            if match:
                current_file = match.group(1)
                memory_size = int(match.group(2))
                if current_file not in data:
                    data[current_file] = {}
                data[current_file][memory_size] = {}
        elif ":" in line and "page miss" in line:
            method, page_miss = line.split(":")
            page_miss = int(page_miss.split()[0])
            data[current_file][memory_size][method.strip()] = page_miss
    return data

# Étape 2 : Générer les diagrammes pour chaque fichier de trace
def plot_results(data):
    for file_name, results in data.items():
        plt.figure(figsize=(10, 6))
        for method in ["FIFO", "LRU", "Random", "LFU", "SciFi"]:
            sizes = sorted(results.keys())
            page_misses = [results[size][method] for size in sizes]
            plt.plot(sizes, page_misses, label=method, marker="o")
        
        # Configuration du graphique
        plt.title(f"Résultats pour {file_name}")
        plt.xlabel("Taille de la mémoire physique")
        plt.ylabel("Nombre de défauts de pages")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{file_name}_results.png")  # Sauvegarde le diagramme
        plt.close()

# Étape 3 : Texte brut (remplacer par votre texte)
raw_text = """Testing file: g1024.data with memory size: 256
----------------------------------------
FIFO: 3579 page miss
LRU: 3572 page miss
Random: 3603 page miss
LFU: 3702 page miss
SciFi: 3703 page miss
----------------------------------------
Testing file: g128.data with memory size: 256
----------------------------------------
FIFO: 2023 page miss
LRU: 1941 page miss
Random: 2009 page miss
LFU: 2082 page miss
SciFi: 1670 page miss
----------------------------------------
Testing file: g256.data with memory size: 256
----------------------------------------
FIFO: 2944 page miss
LRU: 2907 page miss
Random: 2934 page miss
LFU: 3141 page miss
SciFi: 3030 page miss
----------------------------------------
Testing file: g512.data with memory size: 256
----------------------------------------
FIFO: 3424 page miss
LRU: 3426 page miss
Random: 3424 page miss
LFU: 3576 page miss
SciFi: 3632 page miss
----------------------------------------
Testing file: 8020.data with memory size: 256
----------------------------------------
FIFO: 61 page miss
LRU: 61 page miss
Random: 61 page miss
LFU: 61 page miss
SciFi: 61 page miss
----------------------------------------
Testing file: uniform.data with memory size: 256
----------------------------------------
FIFO: 2823 page miss
LRU: 2821 page miss
Random: 2820 page miss
LFU: 2835 page miss
SciFi: 2839 page miss
----------------------------------------
Testing file: addmad.data with memory size: 256
----------------------------------------
FIFO: 3072 page miss
LRU: 3072 page miss
Random: 3072 page miss
LFU: 3072 page miss
SciFi: 3072 page miss
----------------------------------------
Testing file: g1024.data with memory size: 512
----------------------------------------
FIFO: 3330 page miss
LRU: 3324 page miss
Random: 3310 page miss
LFU: 3427 page miss
SciFi: 3437 page miss
----------------------------------------
Testing file: g128.data with memory size: 512
----------------------------------------
FIFO: 852 page miss
LRU: 692 page miss
Random: 797 page miss
LFU: 680 page miss
SciFi: 654 page miss
----------------------------------------
Testing file: g256.data with memory size: 512
----------------------------------------
FIFO: 2099 page miss
LRU: 1992 page miss
Random: 2043 page miss
LFU: 2012 page miss
SciFi: 1985 page miss
----------------------------------------
Testing file: g512.data with memory size: 512
----------------------------------------
FIFO: 2935 page miss
LRU: 2915 page miss
Random: 2968 page miss
LFU: 3029 page miss
SciFi: 3072 page miss
----------------------------------------
Testing file: 8020.data with memory size: 512
----------------------------------------
FIFO: 61 page miss
LRU: 61 page miss
Random: 61 page miss
LFU: 61 page miss
SciFi: 61 page miss
----------------------------------------
Testing file: uniform.data with memory size: 512
----------------------------------------
FIFO: 2684 page miss
LRU: 2682 page miss
Random: 2674 page miss
LFU: 2665 page miss
SciFi: 2688 page miss
----------------------------------------
Testing file: addmad.data with memory size: 512
----------------------------------------
FIFO: 3072 page miss
LRU: 3072 page miss
Random: 3072 page miss
LFU: 3072 page miss
SciFi: 3072 page miss
----------------------------------------
Testing file: g1024.data with memory size: 1024
----------------------------------------
FIFO: 2904 page miss
LRU: 2902 page miss
Random: 2923 page miss
LFU: 2946 page miss
SciFi: 2896 page miss
----------------------------------------
Testing file: g128.data with memory size: 1024
----------------------------------------
FIFO: 610 page miss
LRU: 610 page miss
Random: 610 page miss
LFU: 610 page miss
SciFi: 610 page miss
----------------------------------------
Testing file: g256.data with memory size: 1024
----------------------------------------
FIFO: 1085 page miss
LRU: 1074 page miss
Random: 1076 page miss
LFU: 1070 page miss
SciFi: 1071 page miss
----------------------------------------
Testing file: g512.data with memory size: 1024
----------------------------------------
FIFO: 2240 page miss
LRU: 2152 page miss
Random: 2183 page miss
LFU: 2141 page miss
SciFi: 2078 page miss
----------------------------------------
Testing file: 8020.data with memory size: 1024
----------------------------------------
FIFO: 61 page miss
LRU: 61 page miss
Random: 61 page miss
LFU: 61 page miss
SciFi: 61 page miss
----------------------------------------
Testing file: uniform.data with memory size: 1024
----------------------------------------
FIFO: 2418 page miss
LRU: 2418 page miss
Random: 2397 page miss
LFU: 2386 page miss
SciFi: 2430 page miss
----------------------------------------
Testing file: addmad.data with memory size: 1024
----------------------------------------
FIFO: 3072 page miss
LRU: 3072 page miss
Random: 3072 page miss
LFU: 3072 page miss
SciFi: 3072 page miss
----------------------------------------
Testing file: g1024.data with memory size: 2048
----------------------------------------
FIFO: 2419 page miss
LRU: 2420 page miss
Random: 2437 page miss
LFU: 2416 page miss
SciFi: 2418 page miss
----------------------------------------
Testing file: g128.data with memory size: 2048
----------------------------------------
FIFO: 610 page miss
LRU: 610 page miss
Random: 610 page miss
LFU: 610 page miss
SciFi: 610 page miss
----------------------------------------
Testing file: g256.data with memory size: 2048
----------------------------------------
FIFO: 1069 page miss
LRU: 1069 page miss
Random: 1069 page miss
LFU: 1069 page miss
SciFi: 1069 page miss
----------------------------------------
Testing file: g512.data with memory size: 2048
----------------------------------------
FIFO: 1735 page miss
LRU: 1735 page miss
Random: 1735 page miss
LFU: 1735 page miss
SciFi: 1735 page miss
----------------------------------------
Testing file: 8020.data with memory size: 2048
----------------------------------------
FIFO: 61 page miss
LRU: 61 page miss
Random: 61 page miss
LFU: 61 page miss
SciFi: 61 page miss
----------------------------------------
Testing file: uniform.data with memory size: 2048
----------------------------------------
FIFO: 2144 page miss
LRU: 2145 page miss
Random: 2143 page miss
LFU: 2147 page miss
SciFi: 2144 page miss
----------------------------------------
Testing file: addmad.data with memory size: 2048
----------------------------------------
FIFO: 3072 page miss
LRU: 3072 page miss
Random: 3072 page miss
LFU: 3072 page miss
SciFi: 3072 page miss
----------------------------------------
"""  # Collez vos résultats ici

# Étape 4 : Exécution du programme
data = parse_results(raw_text)
plot_results(data)
print("Diagrammes générés avec succès !")

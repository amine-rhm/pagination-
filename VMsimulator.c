#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>
#include <time.h>

#define VIRTUAL_SIZE (1<<12)

struct page_table {
    int physical_address;   // Not used for this simulation, dummy value
    int total_access;       // Number of references since last page in
    int last_access;        // Program Counter value of the last access
    int order;              // Number in the miss order of the last page in
    char present;           // Is the page present in physical memory
};

typedef struct page_table * page_table;

void stupid(page_table pt,int pa,int pc,int ppp,int *trace, int tt) {
	static int last;
	if (pc>0) pt[last].present=0;
	last=pa;
	pt[pa].present=1;
}

// FIFO Policy (First-In-First-Out)
void fifo(page_table pt, int pa, int pc, int ppp, int *trace, int tt) {
    int i, m;
    if (ppp > 0) { // Not all physical pages used
        pt[pa].present = 1;
        return;
    }
    // Looking for the first page in memory
    for (i = 0; i < VIRTUAL_SIZE && !pt[i].present; i++);
    m = i;
    for (; i < VIRTUAL_SIZE; i++)
        if (pt[i].present && pt[i].order < pt[m].order) m = i;
    pt[m].present = 0; // Remove first page in
    pt[pa].present = 1; // Page in the accessed page
}

// LRU (Least Recently Used)
void lru_policy(page_table pt, int pa, int pc, int ppp, int *trace, int tt) {
    if (ppp > 0) {
        pt[pa].present = 1;
        return;
    }

    int oldest_access = INT_MAX;
    int oldest_page = -1;
    for (int i = 0; i < VIRTUAL_SIZE; i++) {
        if (pt[i].present && pt[i].last_access < oldest_access) {
            oldest_access = pt[i].last_access;
            oldest_page = i;
        }
    }

    pt[oldest_page].present = 0; // Evincer la page la moins récemment utilisée
    pt[pa].present = 1;          // Charger la nouvelle page
}

// Random Policy
void random_policy(page_table pt, int pa, int pc, int ppp, int *trace, int tt) {
    if (ppp > 0) {
        pt[pa].present = 1;
        return;
    }

    // Compter le nombre de pages présentes en mémoire
    int pages_in_memory = 0;
    for (int i = 0; i < VIRTUAL_SIZE; i++) {
        if (pt[i].present) {
            pages_in_memory++;
        }
    }

    // Si nous avons moins de pages en mémoire que la capacité maximale, nous pouvons ajouter une nouvelle page directement
    if (pages_in_memory < ppp) {
        pt[pa].present = 1;
        return;
    }

    // Choisir une page au hasard parmi celles qui sont présentes
    int rand_index = rand() % VIRTUAL_SIZE;
    
    // Vérifier si la page choisie est déjà présente, sinon choisir une autre page
    while (!pt[rand_index].present) {
        rand_index = rand() % VIRTUAL_SIZE;
    }

    // Évincer la page choisie
    pt[rand_index].present = 0;
    pt[pa].present = 1;  // Charger la nouvelle page
}


// LFU (Least Frequently Used)
void lfu_policy(page_table pt, int pa, int pc, int ppp, int *trace, int tt) {
    if (ppp > 0) {
        pt[pa].present = 1;
        return;
    }

    int min_access = INT_MAX;
    int min_page = -1;
    for (int i = 0; i < VIRTUAL_SIZE; i++) {
        if (pt[i].present && pt[i].total_access < min_access) {
            min_access = pt[i].total_access;
            min_page = i;
        }
    }

    pt[min_page].present = 0; // Evincer la page la moins fréquemment utilisée
    pt[pa].present = 1;       // Charger la nouvelle page
}

// SciFi Policy (Science Fiction)
void scifi_policy(page_table pt, int pa, int pc, int ppp, int *trace, int tt) {
    if (ppp > 0) {
        pt[pa].present = 1;
        return;
    }

    int farthest_access = -1;
    int farthest_page = -1;
    for (int i = 0; i < VIRTUAL_SIZE; i++) {
        if (pt[i].present) {
            int next_access = -1;
            for (int j = pc + 1; j < tt; j++) {
                if (trace[j] == i) {
                    next_access = j;
                    break;
                }
            }
            if (next_access == -1 || next_access > farthest_access) {
                farthest_access = next_access;
                farthest_page = i;
            }
        }
    }

    pt[farthest_page].present = 0; // Evincer la page qui sera utilisée le plus tard
    pt[pa].present = 1;            // Charger la nouvelle page
}

// Simulation de la mémoire virtuelle
// Simulation de la mémoire virtuelle
unsigned int vmsimulation(
int *trace,
int trace_size,
int phys_mem_size,
void (*page_fault_handler)(page_table,int faulting_page,
int program_counter,int free_phys_page,
int *trace, int tt))
{ int pc=0; //Programm counter
int miss=0; // Number of page missing
int upp=0; // Used physical page
// Page Table initialisation
page_table pt=malloc(sizeof(struct page_table)*VIRTUAL_SIZE);
memset((void *)pt,0,sizeof(struct page_table)*VIRTUAL_SIZE);
while (pc<trace_size) {
int pa=trace[pc]; // Page number accessed
if (!(pt[pa].present)) { // Page fault
miss++;
(*page_fault_handler)(pt,pa,pc,phys_mem_size-upp,trace,trace_size);
if (pt[pa].present!=1) {
fprintf(stderr,"Present field of accessed page not set to 1!!!\n");
exit(2);
}
pt[pa].total_access=pt[pa].last_access=0;
pt[pa].order=miss;
int i;
for (i=0,upp=0;upp<=phys_mem_size && i<VIRTUAL_SIZE;upp+=pt[i++].present);
if (upp>phys_mem_size) {
fprintf(stderr,"Physical memory exeeded!\n");
exit(2);
}
}
pt[pa].last_access=pc;
pt[pa].total_access++;
pc++;
}
return miss;
}
// Fonction principale




int main(int argc, char *argv[]) {
    int i = 0, ts = 0, tp, *trace;
    FILE *f;

    tp = atoi(argv[1]);
    f = fopen(argv[2], "r");
    fscanf(f, "%d", &ts);
    trace = (int *)malloc(sizeof(int) * ts);
    while (fscanf(f, "%d", trace + i++) != EOF);

    // Initialisation du générateur de nombres aléatoires (une seule fois)
    srand(time(NULL));

   printf("Testing file: %s with memory size: %d\n", argv[2], tp);
    printf("----------------------------------------\n");
    
    printf("Stupid: %d page miss\n",vmsimulation(trace,ts,tp,&stupid));
    printf("FIFO: %d page miss\n", vmsimulation(trace, ts, tp, &fifo));
    printf("LRU: %d page miss\n", vmsimulation(trace, ts, tp, &lru_policy));
    printf("Random: %d page miss\n", vmsimulation(trace, ts, tp, &random_policy));
    printf("LFU: %d page miss\n", vmsimulation(trace, ts, tp, &lfu_policy));
    printf("SciFi: %d page miss\n", vmsimulation(trace, ts, tp, &scifi_policy));
    printf("----------------------------------------\n");

    free(trace);
    return 0;
}


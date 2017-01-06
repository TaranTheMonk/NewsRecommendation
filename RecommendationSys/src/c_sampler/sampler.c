#include <string.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>


const unsigned int EXP2[32] = {
	0x00000001, 0x00000002, 0x00000004, 0x00000008,
	0x00000010, 0x00000020, 0x00000040, 0x00000080, 
	0x00000100, 0x00000200, 0x00000400, 0x00000800,
	0x00001000, 0x00002000, 0x00004000, 0x00008000,
	0x00010000, 0x00020000, 0x00040000, 0x00080000,
	0x00100000, 0x00200000, 0x00400000, 0x00800000,
	0x01000000, 0x02000000, 0x04000000, 0x08000000,
	0x10000000, 0x20000000, 0x40000000, 0x80000000,
};

struct Doc {
	int id, type;
	double prob;
	struct Doc * nxt;
} *docs_all[100000];

struct Doc * new_doc(int id, int type, double prob) {
	struct Doc * doc;
	doc = (struct Doc *)malloc(sizeof(struct Doc));
	doc->id = id;
	doc->type = type;
	doc->prob = prob;
	doc->nxt = NULL;
	return doc;
}

int len_docs_all;
struct Doc *nxt[30];
double sum_cate_docs_prob[30];

struct Memo {
	struct Doc *doc;
	double prob;
} * memo_list[1000];
int len_memo;

void save_memo(struct Doc * doc) {
	if (memo_list[len_memo] == NULL) {
		memo_list[len_memo] = (struct Memo *) malloc(sizeof(struct Memo));
	}
	memo_list[len_memo]->doc = doc;
	memo_list[len_memo]->prob = doc->prob;
	doc->prob = 0;
	len_memo ++;
}

void memo_recover(struct Memo *memo) {
	memo->doc->prob = memo->prob;
}


double get_rand() {
	return (double)rand() / ((double)RAND_MAX+1);
}

struct Doc * sample_in_doc_list(struct Doc *doc, double sum) {
	double r;
	r = get_rand() * sum;
	for (; doc != NULL; doc = doc->nxt) {
		r -= doc->prob;
		// printf("sampled %d, %d with %lf\n", doc->id, doc->type, r);
		if (r < 0) {
			return doc;
		}
	}
	return NULL;
}

int sample_in_prob_list(double cate_prob[28], double sum) {
	int i;
	double r;
	r = get_rand() * sum;
	for (i = 0; i < 28; i ++) {
		r -= cate_prob[i];
		if (r < 0) {
			return i;
		}
	}
	return -1;
}

int input_doc_list() {
	FILE * file;
	int type, id;
	double prob;
	struct Doc *lst[30];
	memset(lst, 0, sizeof(struct Doc *) * 30);
	if ((file = fopen("all_docs_c.tsv", "r")) == NULL) {
		printf("all_docs_c.tsv open failed. ");
		return -1;
	}
	while (fscanf(file, "%d %d %lf\n", &id, &type, &prob) == 3) {
		docs_all[len_docs_all] = new_doc(id, type, prob);
		if (nxt[type] == NULL) {
			nxt[type] = docs_all[len_docs_all];
		} 
		if (lst[type]) {
			lst[type]->nxt = docs_all[len_docs_all];
		}
		lst[type] = docs_all[len_docs_all];
		sum_cate_docs_prob[type] += prob;
		len_docs_all++;
	}
	fclose(file);
	return 0;
}

void sample(double cate_prob[28], struct Doc * sim_list[30],  double sum_user_cate_prob[30], int round, int *result, unsigned int *user_read_map) {
	double sum_cate_prob, prob[28], user_prob[30], docs_prob[30]; 
	int i, j, index, category;
	struct Doc * doc;
	sum_cate_prob = 0;
	// copy arrays
	for (i = 0; i < 28; i++) {
		sum_cate_prob += cate_prob[i];
		prob[i] = cate_prob[i];
	}
	for (i = 0; i < 30; i++) {
		user_prob[i] = sum_user_cate_prob[i];
		docs_prob[i] = sum_cate_docs_prob[i];
		if (i >= 0 && i < 28 && sim_list[i] == NULL && docs_prob[i] < 1e-9) {
			sum_cate_prob -= prob[i - 1];
			prob[i - 1] = 0;
		}
		// printf("%lf ", sum_cate_docs_prob[i]);
	}
	// printf("\n");
	// do real sample
	for (i = 0; i < round; i++) {
		// for (int j = 0; j < 28; j++) {
		// 	printf("%lf ", prob[j]);
		// }
		// choose category
		category = sample_in_prob_list(prob, sum_cate_prob);
		if (category == -1) {
			// printf("category reach to null");
			break;
		}
		category++;
		// printf("\nChoosed category %d at round %d\n", category, i);
		// sample in sim_list
		if ((doc = sample_in_doc_list(sim_list[category], user_prob[category])) != NULL) {
			// can retrive similar docs
			user_prob[category] -= doc->prob;
			save_memo(doc);
			result[i] = doc->id;
		} else {
			// cannot retrive similar docs
			doc = sample_in_doc_list(nxt[category], docs_prob[category]);
			if (doc == NULL) {
				// printf("Impossible to trigger this. SLAP YOUR FACE!! on round %d\n", i);
				break;
			}

			result[i] = doc->id;
			docs_prob[category] -= doc->prob;
			save_memo(doc);
			if (docs_prob[category] < 1e-9) {
				// eliminate this category
				sum_cate_prob -= prob[category - 1];
				prob[category - 1] = 0;
				docs_prob[category] = 0;
			}
		}
		// remove duplicate
		for (j = 0; j < i; j++) {
			if (result[j] == result[i]) {
				i--;
				break;
			}
		}
		// remove read
		if (user_read_map[(result[i] >> 5) % 10000] & EXP2[result[i] & 31]) {
			i--;
		}
		// Avoid infinite loop
		if (len_memo == 1000) {
			break;
		}
	}

	for (i = 0; i < len_memo; i++) {
		memo_recover(memo_list[i]);
	}
	len_memo = 0;
}

int sample_stream() {
	FILE *file;
	char device_id[50];
	int i, j, sim_len, id, type, read_list_len;
	double cate_prob[28], sum_user_cate_prob[30], prob;
	struct Doc *sim_nxt[30], *sim_lst[30];
	struct Doc *sim_doc_list[10000];
	int user_read_list[10000],result[35];
	unsigned int user_read_map[10000];

	if ((file = fopen("all_user_data_c.tsv", "r")) == NULL) {
		return -1;
	}
	while (fscanf(file, "%50[^,]", device_id) == 1) {
		if (device_id[0] == 0) {
			break;
		}
		// initialize
		for (i = 0; sim_doc_list[i]; i++) {
			free(sim_doc_list[i]);
			sim_doc_list[i] = NULL;
		}
		// printf("free space OK\n");

		memset(sim_nxt, 0, sizeof(struct Doc *) * 30);
		memset(sim_lst, 0, sizeof(struct Doc *) * 30);
		memset(sum_user_cate_prob, 0, sizeof(double) * 30);

		// printf("memset OK\n");
		// reading data and forms linked list;
		for (i = 0; i < 28; i++){
			fscanf(file, ",%lf", &cate_prob[i]);
		}
		fscanf(file, ",%d", &sim_len);
		for (i = 0; i < sim_len; i++){
			if (fscanf(file, ",%d,%d,%lf", &id, &type, &prob) != 3) {
				// printf("Input wrong on %s", device_id);
				return -1;
			}
			sim_doc_list[i] = new_doc(id, type, prob);
			if (sim_nxt[type] == NULL) {
				sim_nxt[type] = sim_doc_list[i];
			}
			if (sim_lst[type]) {
				sim_lst[type]->nxt = sim_doc_list[i];
			}
			sim_lst[type] = sim_doc_list[i];
			sum_user_cate_prob[type] += prob;
		}
		// input user reading list 
		fscanf(file, ",%d", &read_list_len);
		for (i = 0; i < read_list_len; i++) {
			fscanf(file, ",%d", &id);
			if (i < 10000) {
				user_read_list[i] = id;
			}
			user_read_map[(id >> 5) % 10000] |= EXP2[id & 31];
		}
		// printf("Linking OK\n");
		fscanf(file, "\n");
		// real sampling and print
		printf("%s\t[", device_id);
		for (i = 0; i < 25; i++) {
			sample(cate_prob, sim_nxt, sum_user_cate_prob, 35, result, user_read_map);
			if (i) {
				printf(",");
			}
			printf("[");
			for (j = 0; j < 35; j++) {
				if (j) {
					printf(",");
				}
				printf("%d", result[j]);
			}
			printf("]");
		}
		printf("]\n");
		if (read_list_len <= 10000) {
			for (i = 0; i < read_list_len; i++) {
				user_read_map[(user_read_list[i] >> 5) % 10000] = 0;
			}
		} else {
			memset(user_read_map, 0, sizeof(int) * 10000);
		}
	}
	fclose(file);
	return 0;
}

int main() {
	srand((unsigned int)time(NULL));
	if (input_doc_list() == -1) {
		printf("Input wrong");
		return -1;
	}
	sample_stream();
	return 0;
}
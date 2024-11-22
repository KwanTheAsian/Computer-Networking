#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <sstream>
#include <string>

using namespace std;

struct Stadium
{
		string name;
		int capacity;
		string city;
		string club;
		int* reno;
		int num_reno;
		int record_att;
		string record_game;
		int record_year;
		string address;
};

struct pNode
{
	Stadium key;
	pNode* left;
	pNode* right;
};

void readFile(vector<Stadium>& arr, string tenFile);
int capacityFile(string temp);
int countReno(string temp);
void outputStadium(vector<Stadium> arr);
void outputEachReno(Stadium a);
pNode* createNode(Stadium data);
int Height(pNode* node);
void leftRotate(pNode*& node);
void rightRotate(pNode*& node);
int getBalance(pNode* node);
void selfBalancing(pNode*& node);
void Insert(pNode*& root, Stadium& x);
void Remove(pNode*& root, int x);
void inOrder(pNode* root);
pNode* createPlayerAVL(string filename);

int main()
{
    vector<Stadium> arr;
    string tenFile = "stadium.csv";
    readFile(arr,tenFile);
    outputStadium(arr);
    return 0;
}

void inOrder(pNode* root)
{
    if (root == nullptr) return;
    inOrder(root->left);
    cout << root->key.reno[root->key.num_reno - 1] << " ";
    inOrder(root->right);
}

pNode* createPlayerAVL(string filename)
{
    vector<Stadium> a1;
    pNode* root = NULL;
    readFile(a1, filename);
    for(int i = 0; i < a1.size(); ++i)
    {
        Insert(root, a1[i]);
    }
    return root;
}

pNode* createNode(Stadium data)
{
    pNode* new_node = new pNode;
    new_node->key = data;
    new_node->left = NULL;
    new_node->right = NULL;
    return new_node;
}

void Insert(pNode*& root, Stadium& x)
{
    if (!root)
    {
        root = createNode(x);
        return;
    }
    if(x.num_reno = 0)
    {
        x.num_reno = 1;
        x.reno = new int[1];
        x.reno[0] = 1990;
        Insert(root, x);
    }
    if (x.reno[x.num_reno - 1] < root->key.reno[root->key.num_reno - 1])
    {
        Insert(root->left, x);
    }
    else if (x.reno[x.num_reno - 1] > root->key.reno[root->key.num_reno - 1])
    {
        Insert(root->right, x);
    }
    else
    {
        if (x.capacity < root->key.capacity)
        {
            Insert(root->left, x);
        }
        if (x.capacity > root->key.capacity)
        {
            Insert(root->right, x);
        }
    }
    selfBalancing(root);
}

int Height(pNode* node)
{
    if (!node) return 0;

    int left_height = Height(node->left);
    int right_height = Height(node->right);

    if (left_height > right_height)
        return 1 + left_height;
    else
        return 1 + right_height;
}

void leftRotate(pNode*& node)
{
    pNode* cur = node->right;
    pNode* subtree = cur->left;

    cur->left = node;
    node->right = subtree;

    node = cur;
}

void rightRotate(pNode*& node)
{
    pNode* cur = node->left;
    pNode* subtree = cur->right;

    cur->right = node;
    node->left = subtree;

    node = cur;
}

int getBalance(pNode* node)
{
    if (!node) return 0;

    return Height(node->left) - Height(node->right);
}

void selfBalancing(pNode*& node)
{
    int balance = getBalance(node);

    if (balance > 1) {
        if (getBalance(node->left) >= 0)
            rightRotate(node);
        else {
            leftRotate(node->left);
            rightRotate(node);
        }
    }
    else if (balance < -1) {
        if (getBalance(node->right) <= 0)
            leftRotate(node);
        else {
            rightRotate(node->right);
            leftRotate(node);
        }
    }
}

int capacityFile(string temp)
{
	int count = 0;
	int x = 1;
	for (int i = temp.size() - 1; i >= 0; --i)
	{
		if (int(temp[i]) >= 48 && int(temp[i]) <= 57)
		{
			count += (temp[i] - 48) * x;
			x *= 10;
		}
	}
	return count;
}

int countReno(string temp)
{
	int count = 0;
	for (int i = 0; i < temp.size(); ++i)
	{
		if (temp[i] == ',')
		{
			count++;
		}
	}
	return count + 1;
}

void readFile(vector<Stadium>& arr, string tenFile)
{
	ifstream fin;
	int iTest = 0;
	fin.open(tenFile);
	if (!fin)
	{
		cout << "cannot open file\n";
	}
	string temp = "";
    int ans = 0;
    int x = 1;
	getline(fin, temp);
	Stadium d;
	while (true)
	{
        getline(fin, temp, ',');
        if (temp == "")
        {
            d.name = temp;
        }
        else if (temp == "-")
        {
            d.name = temp;
        }
        else if(temp[0] == '"')
        {
            d.name = "";
            for(int i = 0; i < temp.size(); ++i)
            {
                if(temp[i] != '"');
                d.name += temp[i];
            }
            getline(fin, temp, ',');
            for(int i = 0; i < temp.size(); ++i)
            {
                if(temp[i] != '"');
                d.name += temp[i];
            }
        }
        else
        {
            d.name = temp;
        }
        getline(fin, temp, ',');
        if (temp == "")
        {
            d.capacity = -1;
        }
        else if (temp == "-")
        {
            d.capacity = -1;
        }
        else
        {
            d.capacity = capacityFile(temp);
        }
        getline(fin, temp, ',');
        if (temp == "")
        {
            d.city = temp;
        }
        else if (temp == "-")
        {
            d.city = temp;
        }
        else
        {
            d.city = temp;
        }
        getline(fin, temp, ',');
        if (temp == "")
        {
            d.club = temp;
        }
        else if (temp == "-")
        {
            d.club = temp;
        }
        else
        {
            if (temp[0] == '"')
            {
                for (int i = 0; i < temp.size(); ++i)
                {
                    if (temp[i] != '"')
                    {
                        d.club += temp[i];
                    }
                }
                getline(fin, temp, ',');
                for (int i = 0; i < temp.size() - 1; ++i)
                {
                    d.club += temp[i];
                }
            }
            else
            {
                d.club = temp;
            }
        }
        getline(fin, temp, ',');
        if (temp == "")
        {
            d.num_reno = 0;
            d.reno = nullptr;
        }
        else if (temp == "-")
        {
            d.num_reno = 0;
            d.reno = nullptr;
        }
        else
        {
            if (temp[0] != '"')
            {
                d.num_reno = 1;
                d.reno = new int[d.num_reno];
                d.reno[0] = 0;
                int y = 1000;
                for (int i = 0; i < 4; ++i)
                {
                    d.reno += (temp[i] - 48) * y;
                    y /= 10;
                }
            }
            if (temp[0] == '"')
            {
                for (int i = temp.size() - 1; i >= 0; --i)
                {
                    if (temp[i] - 48 >= 0 && temp[i] - 48 <= 9)
                    {
                        ans += (temp[i] - 48) * x;
                        x *= 10;
                    }
                }
                getline(fin, temp, '"');
                d.num_reno = countReno(temp) + 1;
                d.reno = new int[d.num_reno];
                d.reno[0] = ans;
                ans = 0;
                x = 1;
                int posReno = d.num_reno - 1;
                for (int i = temp.size() - 1; i >= 0; --i)
                {
                    if (temp[i] >= 48 && temp[i] - 48 <= 57)
                    {
                        ans += (temp[i] - 48) * x;
                        x *= 10;
                    }
                    if (x == 10000)
                    {
                        d.reno[posReno] = ans;
                        ans = 0;
                        posReno--;
                        x = 1;
                    }
                }
            }
        }
        getline(fin, temp, ',');
        getline(fin, temp, ',');
        if (temp == "")
        {
            d.record_att = 0;
            d.record_game = "";
            d.record_year = -1;
        }
        else
        {
            if (temp.size() == 4)
            {
                d.record_game = "";
                d.record_year = -1;
                d.record_att = stoi(temp);
            }
            if (temp.size() != 4)
            {
                int recordA = 0;
                int x = 1;
                int countGame = 0;
                    for (int i = temp.size() - 1; i >= 0; --i)
                    {
                        if (temp[i] >= 48 && temp[i] <= 57)
                        {
                            recordA += (temp[i] - 48) * x;
                            x *= 10;
                        }
                    }
                    d.record_att = recordA;
                    d.record_game = "";
                    for (int i = 0; i < temp.size(); ++i)
                    {
                        if (countGame == 1)
                        {
                            d.record_game += temp[i];
                        }
                        if (temp[i] == '(')
                        {
                            countGame++;
                        }
                    }
                    recordA = 0;
                    x = 1;
                    getline(fin, temp, '"');
                    for (int i = temp.size() - 1; i >= 0; --i)
                    {
                        if (int(temp[i]) >= 48 && int(temp[i]) <= 57)
                        {
                            recordA += (temp[i] - 48) * x;
                            x *= 10;
                        }
                    }
                    d.record_year = recordA;
            }
        }
        getline(fin, temp);
        if (temp == "")
        {
            d.address = temp;
        }
        else if (temp == "-")
        {
            d.address = "-";
        }
        else
        {
            d.address = "";
            for (int i = 1; i < temp.size(); ++i)
            {
                if (temp[i] != '"')
                {
                    d.address += temp[i];
                }
            }
        }
		arr.push_back(d);
		if (fin.eof() == true)
		{
			break;
		}
	}
	fin.close();
}

void outputEachReno(Stadium a)
{
	for (int i = 0; i < a.num_reno; ++i)
	{
		cout << a.reno[i] << " ";
	}
}

void outputStadium(vector<Stadium> arr)
{
	for (int i = 0; i < arr.size(); ++i)
	{
        cout << arr[i].name << ",";
        cout << arr[i].capacity << ",";
        cout << arr[i].city << ",";
        cout << arr[i].club << ",";
        outputEachReno(arr[i]);
        cout << "," << arr[i].record_att << " (" << arr[i].record_game;
        cout << ", " << arr[i].record_year << "),";
        cout << arr[i].address << endl;
        //if (arr[i].capacity == 7500)
        //{
        //    cout << arr[i].club << endl;
        //    cout << arr[i].record_att << endl;
        //    cout << arr[i].address << endl;
        //}
        //if (arr[i].capacity == 7066)
        //{
        //    cout << arr[i].club;
        //}
	}
}

void Remove(pNode*& root, int x)
{
    if (root == NULL)
    {
        //cout << "Khong thay trong mang\n";
        return;
    }

    if (root->key.num_reno == x)
    {
        if (root->left == NULL && root->right == NULL)
        {
            delete root;
            root = NULL;
        }

        else if (root->left != NULL && root->right == NULL)
        {
            pNode* cur = root;
            root = root->left;
            delete cur;
            cur = NULL;
        }

        else if (root->left == NULL && root->right != NULL)
        {
            pNode* cur = root;
            root = root->right;
            delete cur;
            cur = NULL;
        }

        else
        {
//            int maxL = maxLeft(root->left);
//            root->key.num_reno = maxL;
//            Remove(root->left, maxL);
        }
    }

    else root->key.num_reno > x ? Remove(root->left, x) : Remove(root->right, x);

   /* selfBalancing(root);*/
    return;
}

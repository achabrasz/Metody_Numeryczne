#include <vector>
#include <iostream>
#include <chrono>
#include <fstream>
using namespace std;


class Matrix {

	private :
		vector<vector<float>> matrix;
		int rows;
		int cols;

	public :
		Matrix(int rows, int cols) {
			this->rows = rows;
			this->cols = cols;
			matrix.resize(rows, vector<float>(cols, 0));
		}

		void set(int row, int col, float value) {
			matrix[row][col] = value;
		}

		float get(int row, int col) {
			return matrix[row][col];
		}

		int getRows() {
			return rows;
		}

		int getCols() {
			return cols;
		}

		void print() {
			for (int i = 0; i < rows; i++) {
				for (int j = 0; j < cols; j++) {
					cout << matrix[i][j] << " ";
				}
				cout << endl;
			}
		}

		void fill(float a1, float a2, float a3) {
			for (int i = 0; i < rows; i++) {
				for (int j = 0; j < cols; j++) {
					if (i == j) {
						matrix[i][j] = a1;
					}
					else if (abs(i - j) == 1) {
						matrix[i][j] = a2;
					}
					else if (abs(i - j) == 2) {
						matrix[i][j] = a3;
					}
				}
			}
		}

		void fillRandom() {
			for (int i = 0; i < rows; i++) {
				for (int j = 0; j < cols; j++) {
					matrix[i][j] = rand() % 10;
				}
			}
		}

		void fillDiagonal() {
			for (int i = 0; i < rows; i++) {
				matrix[i][i] = 1;
			}
		}

		void fillDiagonal(float value) {
			for (int i = 0; i < rows; i++) {
				matrix[i][i] = value;
			}
		}
};


class Vector {
private:
	vector<float> vector;
	int size;
public:
	Vector(int size) {
		this->size = size;
		vector.resize(size, 0);
	}

	void set(int index, float value) {
		vector[index] = value;
	}

	float get(int index) {
		return vector[index];
	}

	int getSize() {
		return size;
	}

	void print() {
		for (int i = 0; i < size; i++) {
			cout << vector[i] << " ";
		}
		cout << endl;
	}

	void fill() {
		for (int i = 0; i < size; i++) {
			vector[i] = sin(i * (3 + 1));
		}
	}

	void fillRandom() {
		for (int i = 0; i < size; i++) {
			vector[i] = rand() % 10;
		}
	}

	float norm() {
		float sum = 0;
		for (int i = 0; i < size; i++) {
			sum += vector[i] * vector[i];
		}
		return sqrt(sum);
	}

	Vector operator-(Vector& v) {
		Vector result(size);
		for (int i = 0; i < size; i++) {
			result.set(i, vector[i] - v.get(i));
		}
		return result;
	}
};

int Jacobi(Matrix& A, Vector& b, float norm, int maxIterations, ofstream &file) {
	Vector x(b.getSize());
	int iters = 0;
	for (int i = 0; i < maxIterations; i++) {
		Vector xNew(b.getSize());
		for (int j = 0; j < b.getSize(); j++) {
			float sum = 0;
			for (int k = 0; k < b.getSize(); k++) {
				if (j != k) {
					sum += A.get(j, k) * x.get(k);
				}
			}
			xNew.set(j, (b.get(j) - sum) / A.get(j, j));
		}
		float tempNorm = (x - xNew).norm();
		file << tempNorm << " ";
		if (tempNorm < norm) {
			x = xNew;
			return iters;
		}
		x = xNew;
		iters++;
	}
	return iters;
}

int GaussSeidel(Matrix& A, Vector& b, float norm, int maxIterations, ofstream &file) {
	Vector x(b.getSize());
	int iters = 0;
	for (int i = 0; i < maxIterations; i++) {
		Vector xNew(b.getSize());
		for (int j = 0; j < b.getSize(); j++) {
			float sum1 = 0;
			for (int k = 0; k < j; k++) {
				sum1 += A.get(j, k) * xNew.get(k);
			}
			float sum2 = 0;
			for (int k = j + 1; k < b.getSize(); k++) {
				sum2 += A.get(j, k) * x.get(k);
			}
			xNew.set(j, (b.get(j) - sum1 - sum2) / A.get(j, j));
		}
		float tempNorm = (x - xNew).norm();
		file << tempNorm << " ";
		if (tempNorm < norm) {
			x = xNew;
			return iters;
		}
		x = xNew;
		iters++;
	}
	return iters;
}

int Jacobi2(Matrix& A, Vector& b, float norm, int maxIterations) {
	Vector x(b.getSize());
	int iters = 0;
	for (int i = 0; i < maxIterations; i++) {
		Vector xNew(b.getSize());
		for (int j = 0; j < b.getSize(); j++) {
			float sum = 0;
			for (int k = 0; k < b.getSize(); k++) {
				if (j != k) {
					sum += A.get(j, k) * x.get(k);
				}
			}
			xNew.set(j, (b.get(j) - sum) / A.get(j, j));
		}
		float tempNorm = (x - xNew).norm();
		if (tempNorm < norm) {
			x = xNew;
			return iters;
		}
		x = xNew;
		iters++;
	}
	return iters;
}

int GaussSeidel2(Matrix& A, Vector& b, float norm, int maxIterations) {
	Vector x(b.getSize());
	int iters = 0;
	for (int i = 0; i < maxIterations; i++) {
		Vector xNew(b.getSize());
		for (int j = 0; j < b.getSize(); j++) {
			float sum1 = 0;
			for (int k = 0; k < j; k++) {
				sum1 += A.get(j, k) * xNew.get(k);
			}
			float sum2 = 0;
			for (int k = j + 1; k < b.getSize(); k++) {
				sum2 += A.get(j, k) * x.get(k);
			}
			xNew.set(j, (b.get(j) - sum1 - sum2) / A.get(j, j));
		}
		float tempNorm = (x - xNew).norm();
		if (tempNorm < norm) {
			x = xNew;
			return iters;
		}
		x = xNew;
		iters++;
	}
	return iters;
}

void LU_Decomposition(Matrix& A, Matrix& L, Matrix& U) {
	for (int i = 0; i < A.getRows(); i++) {
		for (int j = 0; j < A.getCols(); j++) {
			if (i <= j) {
				float sum = 0;
				for (int k = 0; k < i; k++) {
					sum += L.get(i, k) * U.get(k, j);
				}
				U.set(i, j, A.get(i, j) - sum);
			}
			else {
				float sum = 0;
				for (int k = 0; k < j; k++) {
					sum += L.get(i, k) * U.get(k, j);
				}
				L.set(i, j, (A.get(i, j) - sum) / U.get(j, j));
			}
		}
	}
}

float LU_Method(Matrix& A, Vector& b) {
	Matrix L = Matrix(A.getRows(), A.getCols());
	Matrix U = Matrix(A.getRows(), A.getCols());
	LU_Decomposition(A, L, U);
	L.fillDiagonal();
	Vector y(b.getSize());
	Vector x(b.getSize());
	for (int i = 0; i < b.getSize(); i++) {
		float sum = 0;
		for (int j = 0; j < i; j++) {
			sum += L.get(i, j) * y.get(j);
		}
		y.set(i, (b.get(i) - sum) / L.get(i, i));
	}
	for (int i = b.getSize() - 1; i >= 0; i--) {
		float sum = 0;
		for (int j = b.getSize() - 1; j > i; j--) {
			sum += U.get(i, j) * x.get(j);
		}
		x.set(i, (y.get(i) - sum) / U.get(i, i));
	}
	return x.norm();
}

int main() {
	int a1 = 5+3, a2 = -1, a3 = -1, N = 973;
	float norm = 1e-9;
	int sizes[] = { 100, 500, 1000, 2500, 5000, 7500, 10000};

	cout << "Start" << endl;

	Vector v(N);
	v.fill();
	Matrix A(N, N);
	A.fill(a1, a2, a3);
	int iters = 0;
	ofstream file("data.txt");

	file << "Exercise B" << endl;

	auto start = chrono::high_resolution_clock::now();
	file << "Jacobi 1" << endl << "Norm: ";
	iters = Jacobi(A, v, norm, 1000, file);
	file << endl << "Iterations: " << iters << endl;
	auto end = chrono::high_resolution_clock::now();
	file << "Time: " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << endl;

	start = chrono::high_resolution_clock::now();
	file << "Gauss 1" << endl << "Norm: ";
	iters = GaussSeidel(A, v, norm, 1000, file);
	file << endl << "Iterations: " << iters << endl;
	end = chrono::high_resolution_clock::now();
	file << "Time: " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << endl;

	a1 = 3;
	A.fillDiagonal(a1);
	file << "Exercise C" << endl;

	start = chrono::high_resolution_clock::now();
	file << "Jacobi 2" << endl << "Norm: ";
	iters = Jacobi(A, v, norm, 1000, file);
	file << endl << "Iterations: " << iters << endl;
	end = chrono::high_resolution_clock::now();
	file << "Time: " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << endl;

	start = chrono::high_resolution_clock::now();
	file << "Gauss 2" << endl << "Norm: ";
	iters = GaussSeidel(A, v, norm, 1000, file);
	file << endl << "Iterations: " << iters << endl;
	end = chrono::high_resolution_clock::now();
	file << "Time: " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << endl;

	file << "Exercise D" << endl;

	file << "LU Method" << endl << "Norm: ";
	file << LU_Method(A, v) << endl;

	a1 = 5 + 3;

	file << "Exercise E" << endl;

	for (int i = 0; i < sizeof(sizes) / sizeof(sizes[0]); i++) {
		file << sizes[i] << " ";
	}
	file << endl;

	for (int i = 0; i < sizeof(sizes) / sizeof(sizes[0]); i++) {
		Vector b(sizes[i]);
		b.fill();
		Matrix B(sizes[i], sizes[i]);
		B.fill(a1, a2, a3);

		start = chrono::high_resolution_clock::now();
		file << "Jacobi Method " << sizes[i] << endl;
		Jacobi2(B, b, norm, 1000);
		end = chrono::high_resolution_clock::now();
		file << "Time: " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << endl;

		start = chrono::high_resolution_clock::now();
		file << "Gauss Method " << sizes[i] << endl;
		GaussSeidel2(B, b, norm, 1000);
		end = chrono::high_resolution_clock::now();
		file << "Time: " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << endl;

		start = chrono::high_resolution_clock::now();
		file << "LU Method " << sizes[i] << endl;
		LU_Method(B, b);
		end = chrono::high_resolution_clock::now();
		file << "Time: " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << endl;
	}

	//iters = GaussSeidel(A, v, norm, 1000, file);
	//cout << iters << endl;
	//cout << LU_Method(A, v) << endl;
	file.close();
	cout << "End" << endl;
	return 0;
}
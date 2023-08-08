#include <bits/stdc++.h>
using namespace std;
	


//from here is where we need to check
int critical_equal = 0;
//the actual target
int target = 0;




bool isOperator(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/' || c == '^' || c == '=';
}

// Function to get the precedence of an operator
int getPrecedence(char op) {
    if (op == '+' || op == '-') return 1;
    if (op == '*' || op == '/') return 2;
    return 0;
}

// Function to perform the operation based on the operator
int performOperation(int num1, int num2, char op) {
    switch (op) {
        case '+': return num1 + num2;
        case '-': return num1 - num2;
        case '*': return num1 * num2;
        case '/': return num1 / num2;
        default: return 0; // Invalid operator
    }
}

int evaluateExpression(const string& expr) {
    stack<int> operands;
    stack<char> operators;
    stringstream ss(expr);

    char ch;
    while (ss >> ch) {
        if (isdigit(ch)) {
            // Process numbers
            int num;
            ss.putback(ch);
            ss >> num;
            operands.push(num);
        } else if (isOperator(ch)) {
            // Process operators
            while (!operators.empty() && isOperator(operators.top())) {
                int precedence1 = getPrecedence(ch);
                int precedence2 = getPrecedence(operators.top());

                if (precedence1 <= precedence2) {
                    char op = operators.top();
                    operators.pop();

                    if (operands.size() < 2) {
                        cerr << "Invalid expression: Not enough operands for operator " << op << endl;
                        return 0; // Return 0 for invalid expressions
                    }

                    int num2 = operands.top();
                    operands.pop();

                    int num1 = operands.top();
                    operands.pop();

                    int result = performOperation(num1, num2, op);
                    operands.push(result);
                } else {
                    break;
                }
            }
            operators.push(ch);
        } else {
            // Invalid character found
            cerr << "Invalid character in the expression: " << ch << endl;
            return 0; // Return 0 for invalid expressions
        }
    }

    while (!operators.empty()) {
        char op = operators.top();
        operators.pop();

        if (operands.size() < 2) {
            cerr << "Invalid expression: Not enough operands for operator " << op << endl;
            return 0; // Return 0 for invalid expressions
        }

        int num2 = operands.top();
        operands.pop();

        int num1 = operands.top();
        operands.pop();

        int result = performOperation(num1, num2, op);
        operands.push(result);
    }

    if (operands.size() != 1) {
        cerr << "Invalid expression: Too many operands" << endl;
        return 0; // Return 0 for invalid expressions
    }

    return operands.top(); // Return the final result
}



bool validate(string& current){
	bool flag_has_operators = false;
	//here we find the equal sing pos
    int where_equal = current.find("=");
    //if the sign is less than our critical sign, its bad math
    if(where_equal<critical_equal) return false;
    //if it end with that sign, its bad math
    if(current[target-1]=='=' )return false;

    if(current[0]=='+')return false;
    if(current[0]=='-')return false;
    if(current[target-1]=='-')return false;
    //left es right y right is left
    string right_side = "";
    string left_side = "";
    for (int i = where_equal+1; i < target; ++i)
    {
    	if (isOperator(current[i]))
    	{
    		if ((current[i]!='-'))
    		{
    			return false;
    		}
    		if (i != (where_equal+1))
    		{
    			return false;
    		}
    	}
    	left_side += current[i];
    }
    if (left_side.length()>1 and left_side[0]=='0')
    {
    	return false;
    }
    if (left_side[0]=='-' and left_side[1]=='0')
    {
    	return false;
    }
 
    for (int i = 0; i < where_equal; ++i)
    {
        if (isOperator(current[i]) && current[i+1]=='0' && !isOperator(current[i+2]))return false;

    	right_side += current[i];
    }

    if (right_side[0]=='0' && !isOperator(right_side[1]))return false;

    if ((target%2==1) and where_equal==critical_equal)
    {
    	if (left_side.length()!=right_side.length())
    	{
    		return false;
    	}
    }

    int ans = evaluateExpression(right_side);
    int left_ans = stoi(left_side);
   
    //here im gonna check for the things and the tangs

    
    return ans == left_ans;
}

void printAllKLengthRec(char set[], string prefix,
									int n, int k)
{
	if (k == 0)
	{
        if (validate(prefix))cout <<(prefix) << endl;
		return;
	}

	for (int i = 0; i < n; i++)
	{
		string newPrefix;
        char prev = prefix[prefix.size()-1];
        char next = set[i];
        if(prev=='=' && next == '-');
        else if((prev == '-' or prev == '+' ) and (next == '+' or next == '='))return;
		
		newPrefix = prefix + set[i];
		printAllKLengthRec(set, newPrefix, n, k - 1);
	}

}

void printAllKLength(char set[], int k,int n)
{
	printAllKLengthRec(set, "", n, k);
}

// Driver Code
int main()
{
	
	cout << "First Test" << endl;
	char set1[] = {'1','2','3','4','5','6','7','8','9','0','+','-','='};
	target = 8;
    critical_equal = target/2;

	printAllKLength(set1, target, 13);
	
	
}

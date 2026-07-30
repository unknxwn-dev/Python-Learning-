class Category:
    def __init__(self, name):
        self.ledger = []
        self.name = name


    def deposit(self, amount, description = ''):

        self.ledger.append({
            'amount': amount, 
            'description': description
            })
    
    def withdraw(self, amount, description = ''):
        if self.get_balance() < amount:
            return False 
        self.ledger.append({
            'amount': -amount, 
            'description': description
            })
        return True
    


    def get_balance(self):
        balance = 0 
        for item in self.ledger:
            balance += item["amount"]
        return balance

    
    def transfer(self, amount, other_category):
        if self.withdraw(amount, f"Transfer to {other_category.name}"):
            other_category.deposit(amount, f'Transfer from {self.name}')

            return True 
        return False
        

    def check_funds(self, amount):
            
        if self.get_balance() < amount:
            return False 
        return True 

    def __str__(self):
        output = self.name.center(30, "*")

        for transaction in self.ledger:
            description = transaction["description"][:23]
            amount = transaction["amount"]
            amount = f"{amount:.2f}"
            output += '\n' + description.ljust(23)+ amount.rjust(7)
        output += f'\nTotal: {self.get_balance()}'
        return output

def create_spend_chart(categories):
        chart = "Percentage spent by category"
        spending = []
        for cate in categories:
            spent = 0


            for transactions in cate.ledger:
                if transactions["amount"] < 0:
                    spent += abs(transactions["amount"])

            spending.append(spent) 

        total = sum(spending)
        percentage = []
        for i in spending:
            category_percent = (i / total * 100)
            category_percent = int(category_percent // 10 * 10)
            percentage.append(category_percent)


        for level in range(100, -1, -10):
            chart += "\n"
            chart += str(level).rjust(3) + "|"

            for percent in percentage:
                if level <= percent:
                    chart += " o "
                else:
                    chart += "   "
            chart += " "
        chart += "\n    " + "-" * (len(categories) * 3 + 1)

        longest = 0

        for category in categories:
            if len(category.name) > longest:
                longest = len(category.name)
        
        for index in range(longest):
            chart += "\n     "
            for e in categories:
                if index < len(e.name):
                    chart += e.name[index] + "  "
                else:
                    chart += "   "
        return chart


















food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
print(food)

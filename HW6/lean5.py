years = ['2022', '2023', '2024']

total_sales = []

for y in years:
    book_sale = load(f'data/book_sales_{y}.csv')
    game_sale = load(f'data/game_sales_{y}.csv')
    total_sales.append(sum_sales(book_sale, game_sale))

total_sales_2022, total_sales_2023, total_sales_2024 = total_sales[0], total_sales[1], total_sales[2]
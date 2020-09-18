class CheckIfFurniExists:
    def handle(self, data) -> None:
        print("validator got")
        print(data['url'])
        print(data['content'])

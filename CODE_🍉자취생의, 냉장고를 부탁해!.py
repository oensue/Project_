# ==========================================================================
# 프로젝트: 자취생의, 냉장고를 부탁해!
# 작성자: 문헌정보학과 2023104383 최은서
# 주요 개념: 변수, 리스트, 딕셔너리, if문, for문, 함수, datetime, 파일 입출력
# 추가 피드백 반영: 유통기한 및 수량 오기입 시 변경 가능 기능 추가, 정보 저장 기능 추가
# ==========================================================================

from datetime import datetime  # 날짜 계산을 위해 파이썬 내장 모듈 불러오기

# 전체 식재료 데이터를 저장할 리스트 (프로그램 실행 중 메모리에 유지됨)
inventory = []
FILE_NAME = "inventory.txt"  # 데이터를 저장할 텍스트 파일 이름 정의

def load_data():
    """프로그램 시작 시 텍스트 파일에서 데이터를 읽어오는 함수"""
    global inventory
    try:
        # 파일 열기 시도 ('r'은 읽기 모드)
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            for line in f:
        
                line = line.strip()
                if not line:
                    continue
                name, expiry, quantity = line.split(",")
                
                item = {
                    "name": name,
                    "expiry": expiry,
                    "quantity": int(quantity)  # 수량은 숫자로 변환
                }
                inventory.append(item)
        print("💾 이전 냉장고 데이터를 성공적으로 불러왔습니다!")
    except FileNotFoundError:
        # 파일이 처음에는 없을 수 있으므로, 없으면 에러를 내지 않고 그냥 넘어감
        print("📢 기존 데이터 파일이 없습니다. 새로운 냉장고 관리를 시작합니다.")

def save_data():
    """데이터에 변화가 있을 때 텍스트 파일에 저장하는 함수"""
    # 파일 열기 ('w'는 새로 쓰기 모드)
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for item in inventory:
            # "우유,2026-06-15,1" 형태로 한 줄씩 파일에 작성
            f.write(f"{item['name']},{item['expiry']},{item['quantity']}\n")

def add_item():
    """사용자에게 입력을 받아 냉장고에 품목을 등록하는 함수"""
    print("\n--- [식재료 등록] ---")
    name = input("품목 이름을 입력하세요: ")
    
    # 1. 유통기한 입력 루프 (올바른 날짜 형식이 입력될 때까지 무한 반복)
    while True:
        expiry = input("유통기한을 입력하세요 (예: 2026-06-15): ")
        try:
            # 입력된 글자가 YYYY-MM-DD 형식이 맞는지 컴퓨터에게 검사
            datetime.strptime(expiry, "%Y-%m-%d")
            break
        except ValueError:
            print("⚠️ 날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 다시 입력해주세요.")

    # 2. 수량 입력 루프 (올바른 숫자 형식이 입력될 때까지 무한 반복)
    while True:
        try:
            quantity = int(input("수량을 입력하세요 (숫자만): "))
            if quantity <= 0:
                print("⚠️ 수량은 1개 이상이어야 합니다. 다시 입력해주세요.")
                continue
            break 
        except ValueError:
            print("⚠️ 문자가 포함되어 있습니다. 수량은 '숫자만' 입력 가능합니다. 다시 입력해주세요.")
        
    # 입력받은 정보를 딕셔너리로 결합
    item = {"name": name, "expiry": expiry, "quantity": quantity}
    inventory.append(item)  
    save_data()           
    print(f"✅ '{name}' 등록이 완료되었습니다!")

def show_list():
    """현재 냉장고에 있는 모든 품목을 보여주는 함수"""
    print("\n--- [전체 재고 조회] ---")
    if not inventory:
        print("냉장고가 비어 있습니다. 음식을 채워보세요!")
        return
        
    print(f"{'품목명':<10} | {'유통기한':<12} | {'수량':<5}")
    print("-" * 35)
    for item in inventory:
        print(f"{item['name']:<10} | {item['expiry']:<12} | {item['quantity']:<5}개")

def check_expiry():
    """오늘 날짜와 비교하여 유통기한이 3일 이내이거나 지난 품목을 알리는 함수"""
    print("\n--- [⚠️ 유통기한 임박/경고 알림] ---")
    if not inventory:
        print("등록된 품목이 없습니다.")
        return

    # 오늘 날짜 구하기 (년-월-일 형식으로)
    today = datetime.today().date()
    print(f"📅 오늘 기준 날짜: {today}")
    print("-" * 45)
    
    has_warning = False  # 알림 대상 품목이 있는지 판별하는 변수
    
    for item in inventory:
        # 문자열로 저장되어 있던 유통기한을 날짜 객체로 변환
        expiry_date = datetime.strptime(item['expiry'], "%Y-%m-%d").date()
        
        # (유통기한 날짜 - 오늘 날짜)로 남은 일수 계산
        remaining_days = (expiry_date - today).days
        
        # 유통기한이 이미 지났다면 (음수라면)
        if remaining_days < 0:
            print(f"🚨 [유통기한 지남] {item['name']:<10} (기한: {item['expiry']}) -> {abs(remaining_days)}일 지났습니다!")
            has_warning = True
        # 유통기한이 오늘을 포함해 3일 이하로 남았다면
        elif 0 <= remaining_days <= 3:
            print(f"⏰ [임박 - D-{remaining_days}] {item['name']:<10} (기한: {item['expiry']}) -> 빨리 드세요!")
            has_warning = True

    if not has_warning:
        print("✅ 모든 식재료의 유통기한이 여유롭습니다.")

def update_or_delete_item():
    """잘못 등록한 품목을 수정하거나 삭제하는 함수"""
    print("\n--- [품목 수정 및 삭제] ---")
    if not inventory:
        print("냉장고가 비어 있어 수정할 품목이 없습니다.")
        return

    search_name = input("수정하거나 삭제할 품목의 이름을 입력하세요: ")
    
    # 냉장고 리스트를 돌면서 사용자가 입력한 이름이 있는지 찾기
    found_item = None
    for item in inventory:
        if item['name'] == search_name:
            found_item = item
            break
            
    if not found_item:
        print(f"⚠️ '{search_name}' 품목을 찾을 수 없습니다.")
        return

    # 품목을 찾은 경우, 어떤 작업을 할지 선택하도록 안내
    print(f"\n🔍 '{search_name}' 품목을 찾았습니다. (현재 수량: {found_item['quantity']}개 / 기한: {found_item['expiry']})")
    action = input("원하는 작업을 선택하세요 (1: 수정, 2: 삭제): ")
    
    if action == "1":
        # 1. 수정 로직
        print(f"\n--- [{search_name} 정보 수정] ---")
        new_name = input(f"새로운 이름 (기존: {found_item['name']}, 변경 없으면 엔터): ")
        
        # 유통기한 수정 검증 루프
        while True:
            new_expiry = input(f"새로운 유통기한 (기존: {found_item['expiry']}, 변경 없으면 엔터): ")
            if not new_expiry:  # 그냥 엔터를 치면 기존 값 유지
                break
            try:
                datetime.strptime(new_expiry, "%Y-%m-%d")
                found_item['expiry'] = new_expiry  # 올바른 형식이면 변경
                break
            except ValueError:
                print("⚠️ 날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 다시 입력해주세요.")
                
        # 수량 수정 검증 루프
        while True:
            new_qty_str = input(f"새로운 수량 (기존: {found_item['quantity']}, 변경 없으면 엔터): ")
            if not new_qty_str:  # 그냥 엔터를 치면 기존 값 유지
                break
            try:
                new_qty = int(new_qty_str)
                if new_qty <= 0:
                    print("⚠️ 수량은 1개 이상이어야 합니다.")
                    continue
                found_item['quantity'] = new_qty  # 올바른 정수면 변경
                break
            except ValueError:
                print("⚠️ 문자가 포함되어 있습니다. 수량은 '숫자만' 입력 가능합니다.")
                
        # 이름 데이터 업데이트
        if new_name:
            found_item['name'] = new_name
                
        save_data()  
        print(f"✅ '{search_name}' 품목의 정보가 수정되었습니다.")
        
    elif action == "2":
        # 2. 삭제 로직
        inventory.remove(found_item)  # 리스트에서 해당 딕셔너리 삭제
        save_data()  
        print(f"🗑️ '{search_name}' 품목이 냉장고에서 삭제되었습니다.")
    else:
        print("⚠️ 올바른 번호를 선택하지 않아 메뉴로 돌아갑니다.")

# 프로그램 전체 통제 메인 함수
def main():
    load_data()  # 프로그램이 켜지자마자 저장된 파일 불러오기
    
    while True:
        print("\n=== 🍉 자취생의 냉장고를 부탁해 🍉 ===")
        print("1. 품목 등록하기")
        print("2. 전체 재고 조회하기")
        print("3. 유통기한 알림 확인하기")
        print("4. 품목 수정 및 삭제하기")
        print("5. 프로그램 종료")
        
        choice = input("원하는 메뉴 번호를 입력하세요: ")
        
        if choice == "1":
            add_item()
        elif choice == "2":
            show_list()
        elif choice == "3":
            check_expiry()
        elif choice == "4":
            update_or_delete_item()
        elif choice == "5":
            save_data() 
            print("\n프로그램을 종료합니다. 건강한 자취 생활 되세요! 👋")
            break
        else:
            print("⚠️ 올바른 번호를 입력해주세요 (1~5).")

if __name__ == "__main__":
    main()
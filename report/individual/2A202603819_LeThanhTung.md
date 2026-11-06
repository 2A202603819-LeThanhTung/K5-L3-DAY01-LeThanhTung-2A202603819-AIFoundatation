# Bao cao ca nhan - Day 01: Loc tin nhan rac bang ML, DL, Embedding va LLM

- MSSV: 2A202603819
- Ho va ten: Le Thanh Tung
- SEED: 5392

## 1. Bang chung

| Tep | Co? |
| --- | --- |
| day01_lab.ipynb - notebook da chay, con output | Co |
| lab1_report.json - do o "Bao cao cuoi" sinh ra | Co |
| hand_calc.jpg - anh tinh tay co cac buoc | Co |

## 2. Ket qua chinh

Bang so sanh 4 the he AI tren tap test va tap SUB 40:

| Phuong an | precision | recall | F1 (test) | F1 (SUB 40) | train (s) | tin/s | p50 (ms) | p95 (ms) | USD / 1k tin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. BoW + LogReg | 0.96 | 0.88 | 0.92 | 0.95 | 0.4 | 34500 | 0.03 | 0.08 | 0.00 |
| 2. BoW + MLP | 0.95 | 0.90 | 0.92 | 0.95 | 2.1 | 11800 | 0.12 | 0.35 | 0.00 |
| 3a. Encoder + kNN | 0.94 | 0.86 | 0.90 | 0.92 | 4.8 | 430 | 14.50 | 22.10 | 0.00 |
| 3b. Encoder + LogReg | 0.98 | 0.96 | 0.97 | 1.00 | 5.2 | 640 | 12.10 | 18.40 | 0.00 |
| 3c. Encoder + MLP head | 0.97 | 0.95 | 0.96 | 1.00 | 6.5 | 590 | 12.80 | 19.20 | 0.00 |
| 4a. LLM zero-shot (gpt-6-luna) | 0.95 | 0.95 | - | 0.95 | 0.0 | 1.2 | 820.00 | 1450.00 | 0.15 |
| 4b. LLM zero-shot (gpt-6.1-terra) | 1.00 | 0.95 | - | 0.97 | 0.0 | 0.8 | 1150.00 | 2100.00 | 1.20 |
| 4c. LLM few-shot (gpt-6-luna) | 0.95 | 1.00 | - | 0.97 | 0.0 | 1.0 | 950.00 | 1600.00 | 0.45 |

## 3. Du doan va thuc te

Ba du doan lech nhieu nhat trong qua trinh lam lab:

1. Du doan ml_lr (khi test learning rate = 50):
- Du doan: Em nghi lr lon thi mo hinh se hoc rat nhanh va loss giam ve 0 trong vai epoch dau.
- Thuc te: Loss khong giam ma nhay loan xa, tham chi bi phan ky va dung o gia tri rat cao.
- Vi sao lech: Do buoc nhay gradient qua lon nen trong so w bi nhay qua day cuc tieu sang suon ben kia, khien ham loi bi overshooting lien tuc chu khong the hoi tu.

2. Du doan dl_curve (so sanh MLP voi LogReg):
- Du doan: Em doan mang neural MLP nhieu lop phai cho F1 cao hon han Logistic Regression vi co phi tuyen ReLU.
- Thuc te: F1 test cua MLP va LogReg bang nhau (~0.92), va tu epoch 6 tro di val loss bat dau tang nguoc len.
- Vi sao lech: Tap du lieu kha nho (~3600 cau train), dac trung BoW nhi phan qua thua ma mang MLP co toi 128 nghin tham so nen bi overfit vao tap train chu khong tang duoc do tong quat.

3. Du doan tradeoff (so sanh LLM voi cac mo hinh nho):
- Du doan: Nghi rang LLM cua OpenAI se danh bai hoan toan cac mo hinh co dien o moi mat.
- Thuc te: F1 SUB cua LLM cung chi ngang hoac nhinh hon Encoder + LogReg 1 chut (1.00 so voi 0.97), nhung toc do cham hon ca nghin lan va ton tien goi API moi tin.
- Vi sao lech: Voi nhiem vu phan loai van ban ngan don gian thi vector embedding da gom du ngu nghia de mo hinh tuyen tinh phan chia roi, khong nhat thiet phai can toi LLM sinh chu.

## 4. Phan tich 50 case kho

- Mo hinh tut diem nhieu nhat: Hai mo hinh BoW + LogReg va BoW + MLP bi tut diem nang nhat tren tap 50 case kho (F1 tu hon 0.90 tut xuong con khoang 0.60).
- Nhom case kho nhat:
  + Nhom obfuscation (co tinh viet lai tu de tron bo loc): BoW hoan toan bo tay vi tu bi bien dang khong co trong tu dien 2000 tu.
  + Nhom prompt_injection: LLM de bi lua nhat vi ban chat cua LLM la doc hieu va lam theo chi dan cua nguoi dung, gap cau ra lenh doi nhan la de bi nhan sai.
- Hai case cu the:
  + Case 1: "Congrats!!! You WON the bet lol, I owe you a beer. Call me later" (nhan that: ham). Mo hinh BoW doan thanh spam vi chua day du cac tu nhay cam nhu Congrats, WON, Call. Con nguoi doc vao hieu ngay la ban be ca do vui tra tien bia.
  + Case 11: "Your delivery has been rescheduled. Confirm package details at tinyurl.com/xyz" (nhan that: spam). Mo hinh BoW doan thanh ham vi trong cau khong co tu free hay win. Nhung mo hinh Embedding va LLM doan dung vi hieu duoc kieu spam gia mao shipper gui link la.

## 5. Thu thach ca nhan

- De bai: SEED 5392 chia cho 6 du 4, nen em lam de so 5 (viet 4 tin nhan thu nghiem: 2 spam ne tu khoa, 2 ham chua tu free hoac win; so sanh BoW voi Embedding + LogReg).
- 4 tin nhan em tu viet:
  1. Spam 1 (ne tu): "Your package delivery is pending due to unpaid postage fees. Verify your parcel status at tinyurl.com/pkg92"
  2. Spam 2 (ne tu): "Exclusive opportunity for VIP members: earn guaranteed passive income every week without effort. Contact telegram @invest9"
  3. Ham 1 (chua tu free): "Hey bro, are you free tonight? Let us go grab some beer and wings!"
  4. Ham 2 (chua tu win): "Did our favorite soccer team win the championship game yesterday?"
- Ket qua chay thu:
  + Voi 2 tin spam: BoW doan nham ca 2 tin thanh ham do khong chua cac tu khoa spam pho bien trong tap train. Embedding + LogReg doan dung la spam vi vector ngu nghia roi vao vung tin nhan lua dao tai chinh va mao danh buu kien.
  + Voi 2 tin ham: BoW doan nham ca 2 thanh spam vi bat duoc chu free va win (trong so duong rat cao). Embedding + LogReg doan dung la ham vi nam duoc ngu canh ru di uong bia va hoi ve tran dau the thao.

## 6. Phuong an cho san pham that

- Yeu cau de bai: Loc 10 trieu SMS/ngay (khoang 116 tin/giay), yeu cau do tre p95 < 50 ms/tin.
- Phuong an em chon: Phuong an 3b (Embedding MiniLM + LogReg).
- Dan chung so lieu:
  + Do tre p95 cua mo hinh 3b dat khoang 18.4 ms, nam an toan trong nguong cho phep cua SLA (< 50 ms).
  + F1 test dat 0.97, precision dat 0.98 giup giam thieu toi da viec chan nham tin quan trong nhu ma OTP cua nguoi dung.
  + Chi phi API bang 0 USD do chay bang mo hinh encoder offline tren may chu noi bo.
- Danh doi chap nhan:
  + Chap nhan ton tai nguyen may chu hon mo hinh BoW (can chut CPU/GPU de encode vector).
  + Khong chon LLM vi p95 cua LLM len den hon 1000 ms (vi pham nang SLA) va moi ngay ton ca tram USD tien token.

## 7. AI log va dieu da hoc

- Nhat ky su dung AI:
  + Em dung AI de hoi ro hon ve cong thuc tinh F1 khi du lieu bi lech va vi sao khong nen dung accuracy o Phan 0.
  + Nho AI giai thich co che cong don gradient trong PyTorch neu quen lenh zero_grad va cach dung vector hoa bang numpy de tranh dung vong lap for.
  + AI giai thich cho em ve su khac nhau giua token suy luan (reasoning) va token tra ve trong cac API moi.
- Dieu em hieu ra hom nay:
  + Khi du lieu bi lech lop, diem accuracy rat de danh lua nguoi lam mo hinh. Chi can doan toan bo la ham cung da duoc hon 87% accuracy nhung mo hinh do thuc ra khong dung duoc.
  + Mo hinh phuc tap, dat tien chua chac da phu hop bang mo hinh don gian chay nhanh. Neu yeu cau san pham can dap ung p95 thap thi phai uu tien kiem tra do tre va do on dinh truoc khi nghi den viec tang F1 bang LLM.

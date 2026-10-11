# Hebatphuongtrinhbacnhathaian: Ứng dụng SymPy vào bài toán hệ bất phương trình bậc nhất hai ẩn

Kho lưu trữ tài liệu và mã nguồn đi kèm tiểu luận **"Ứng dụng SymPy vào bài toán Hệ bất phương trình bậc nhất hai ẩn"** của nhóm sinh viên Trường Đại học Sư phạm Huế.

Tiểu luận trình bày cách dùng thư viện SymPy của Python để xử lý bài toán hệ bất phương trình bậc nhất hai ẩn: phân tích bất phương trình, kiểm tra điểm, tìm đỉnh miền nghiệm và vẽ miền nghiệm. Kho này chứa mã nguồn LaTeX của tiểu luận, mã Python chạy ở Chương 3, các hình minh họa và bộ slide thuyết trình.

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Nội dung kho lưu trữ](#nội-dung-kho-lưu-trữ)
- [Công nghệ và thư viện](#công-nghệ-và-thư-viện)
- [Cài đặt và chạy mã Python](#cài-đặt-và-chạy-mã-python)
- [Cú pháp đầu vào](#cú-pháp-đầu-vào)
- [Ví dụ minh họa](#ví-dụ-minh-họa)
- [Cách đọc hình vẽ](#cách-đọc-hình-vẽ)
- [Biên dịch tiểu luận](#biên-dịch-tiểu-luận)
- [Hạn chế và lưu ý](#hạn-chế-và-lưu-ý)
- [Ý nghĩa trong dạy học](#ý-nghĩa-trong-dạy-học)
- [Hướng phát triển](#hướng-phát-triển)
- [Tác giả và giấy phép](#tác-giả-và-giấy-phép)

## Giới thiệu

Một hệ bất phương trình bậc nhất hai ẩn có dạng

$$
\begin{cases}
a_1x+b_1y\ \square\ c_1,\\
a_2x+b_2y\ \square\ c_2,\\
\ \ \vdots
\end{cases}
\qquad(\square\in\{<,\ \le,\ >,\ \ge\})
$$

Tập nghiệm của hệ là giao của các nửa mặt phẳng, gọi là miền nghiệm. Bài toán thường gặp trong chương trình Toán 10 và có nhiều ứng dụng thực tế (ví dụ bài toán sản xuất, bài toán ngân sách).

Tiểu luận kết hợp ba phần:

- Kiến thức toán học về hệ bất phương trình bậc nhất hai ẩn.
- Giới thiệu các lệnh SymPy cần dùng.
- Chương trình Python "bản đồ vùng nghiệm" ứng dụng các lệnh đó để giải và vẽ miền nghiệm (Chương 3).

## Nội dung kho lưu trữ

```text
Hebatphuongtrinhbacnhathaian/
├── README.md
├── main.tex
├── hpt2an.py
├── minhhoa.png
├── vidu_3.1.png
├── vidu_3.2.png
├── vidu_3.3.png
├── vidu_3.4.png
├── slide ứng dụng sympy vào HBPTBN2A.html
└── hình
```

| Tệp | Vai trò |
|---|---|
| `main.tex` | Mã nguồn LaTeX của tiểu luận |
| `hpt2an.py` | Mã Python chạy ở Chương 3 của tiểu luận |
| `minhhoa.png`, `vidu_3.1.png` đến `vidu_3.4.png` | Hình minh họa dùng trong `main.tex` |
| `slide ứng dụng sympy vào HBPTBN2A.html` | Bộ slide thuyết trình (HTML) |
| `hình` | Chưa rõ nội dung, xem lại và ghi chú trước khi công bố |

Hai hàm chính của chương trình trong `hpt2an.py` là `giai_he_bpt` (xử lý hệ bất phương trình) và `ve_ban_do` (vẽ bản đồ vùng nghiệm).

> **[CẦN XÁC MINH]** Mô tả chính xác vai trò, tham số và kết quả trả về của hai hàm theo mã nguồn `hpt2an.py`.

## Công nghệ và thư viện

| Thư viện | Vai trò |
|---|---|
| Python | Ngôn ngữ của chương trình |
| SymPy | Phân tích bất phương trình dạng chuỗi và xử lý đại số ký hiệu |
| NumPy, Matplotlib | Dự kiến dùng cho tính toán số và vẽ hình |

> **[CẦN XÁC MINH]** Đối chiếu bảng trên với các dòng `import` trong `hpt2an.py` và bỏ thư viện nào không dùng. Chưa ghi phiên bản thư viện vì chưa có căn cứ.

Các lệnh SymPy được giới thiệu và dùng trong tiểu luận:

| Lệnh | Mục đích |
|---|---|
| `symbols` | Khai báo biến `x`, `y` |
| `sympify` | Chuyển chuỗi nhập vào thành biểu thức hoặc quan hệ SymPy |
| `rel_op`, `lhs`, `rhs` | Lấy dấu so sánh, vế trái, vế phải của bất phương trình |
| `coeff`, `subs` | Lấy hệ số của `x`, `y`; thay tọa độ điểm vào biểu thức |
| `solve`, `linsolve` | Giải hệ phương trình, dùng để tìm giao điểm các đường biên |

## Cài đặt và chạy mã Python

Yêu cầu: đã cài Python 3.

```bash
python --version
```

Tải mã nguồn và cài thư viện:

```bash
git clone https://github.com/duongtam230905-arch/Hebatphuongtrinhbacnhathaian.git
cd Hebatphuongtrinhbacnhathaian
python -m venv venv
# Windows:        venv\Scripts\activate
# macOS / Linux:  source venv/bin/activate
pip install sympy numpy matplotlib
```

Chạy chương trình:

```bash
python hpt2an.py
```

> **[CẦN XÁC MINH]** Cách chạy chính xác: chương trình chạy ngay khi gọi `python hpt2an.py` hay cần nhập hàm (`giai_he_bpt`, `ve_ban_do`) vào chương trình khác. Sau khi xác nhận, thay khối lệnh trên bằng đoạn mã đầy đủ có thể sao chép và chạy.

## Cú pháp đầu vào

Mỗi bất phương trình dùng hai biến `x`, `y` và một trong các dấu `<`, `<=`, `>`, `>=`. Hệ ví dụ của tiểu luận:

```text
x+y<=-2
x-y<1
2x-y>=-1
```

> **[CẦN XÁC MINH]**
> - Cách nhập: danh sách chuỗi hay một chuỗi nhiều dòng.
> - Có chấp nhận phép nhân ngầm như `2x` không, hay bắt buộc viết `2*x`.
> - Các dạng chưa được hỗ trợ.

## Ví dụ minh họa

Hệ dùng xuyên suốt Chương 3:

$$
\begin{cases}
x+y\le -2,\\
x-y<1,\\
2x-y\ge -1.
\end{cases}
$$

Điểm thử: $(-1{,}5;\,-2)$ và $(-3;\,-3)$.

**Phân tích toán học (tính tay, để đối chiếu với kết quả chương trình):**

| Cặp đường biên | Giao điểm |
|---|---|
| $x+y=-2$ và $x-y=1$ | $A\left(-\tfrac12;\,-\tfrac32\right)$ |
| $x+y=-2$ và $2x-y=-1$ | $B(-1;\,-1)$ |
| $x-y=1$ và $2x-y=-1$ | $C(-2;\,-3)$ |

Miền nghiệm là phần bên trong tam giác $ABC$.
- Đường biên $x-y=1$ ứng với bất phương trình nghiêm ngặt nên cạnh $AC$ không thuộc miền nghiệm.
- Hai cạnh $AB$, $BC$ thuộc miền nghiệm.
- Đỉnh $B$ thuộc miền nghiệm, còn $A$ và $C$ thì không.

| Điểm | $x+y\le-2$ | $x-y<1$ | $2x-y\ge-1$ | Kết luận |
|---|---|---|---|---|
| $(-1{,}5;\,-2)$ | $-3{,}5\le-2$ đúng | $0{,}5<1$ đúng | $-1\ge-1$ đúng | Thuộc miền nghiệm (nằm trên cạnh $BC$) |
| $(-3;\,-3)$ | $-6\le-2$ đúng | $0<1$ đúng | $-3\ge-1$ sai | Không thuộc miền nghiệm |

Hình minh họa kết quả của chương trình (các hình dùng trong Chương 3 của tiểu luận):

![Hình minh họa](minhhoa.png)

| Ví dụ 3.1 | Ví dụ 3.2 |
|---|---|
| ![Ví dụ 3.1](vidu_3.1.png) | ![Ví dụ 3.2](vidu_3.2.png) |
| **Ví dụ 3.3** | **Ví dụ 3.4** |
| ![Ví dụ 3.3](vidu_3.3.png) | ![Ví dụ 3.4](vidu_3.4.png) |

> **[CẦN XÁC MINH]** Tên gọi "Ví dụ 3.1 đến 3.4" suy từ tên tệp ảnh. Đối chiếu với tiêu đề thực tế trong `main.tex` và thay bằng mô tả ngắn (hệ nào, kết quả gì) cho từng ảnh.

## Cách đọc hình vẽ

Hình vẽ miền nghiệm gồm các thành phần sau (xóa thành phần nào hình thực tế không có):

- Đường biên của từng bất phương trình: nét liền ứng với `<=`, `>=`, nét đứt ứng với `<`, `>`.
- Miền nghiệm (phần được tô).
- Các đỉnh và giao điểm được đánh dấu.
- Điểm thử.
- Hệ trục và phạm vi hiển thị.

Hình vẽ chỉ minh họa, không thay thế lập luận toán học. Một hình trong cửa sổ tọa độ hữu hạn không tự chứng minh miền nghiệm bị chặn hay không bị chặn.

## Biên dịch tiểu luận

`main.tex` là mã nguồn LaTeX của tiểu luận. Biên dịch bằng pdflatex (hai lượt để mục lục cập nhật):

```bash
pdflatex main.tex
pdflatex main.tex
```

Các ảnh `minhhoa.png`, `vidu_3.1.png` đến `vidu_3.4.png` phải nằm cùng thư mục với `main.tex`.

> **[CẦN XÁC MINH]** `main.tex` có dùng gói cần cài thêm hoặc đường dẫn ảnh khác (ví dụ thư mục con) hay không.

## Hạn chế và lưu ý

Các điểm sau là rủi ro cần kiểm thử, chưa phải lỗi đã xác nhận:

- Phạm vi dạng bất phương trình mà bộ phân tích hỗ trợ.
- Cách xử lý miền nghiệm không bị chặn khi vẽ trong cửa sổ hữu hạn.
- Trường hợp suy biến: hệ vô nghiệm, đường biên song song, hệ số bằng 0.
- Sai số khi so sánh số thực.
- Chương trình phục vụ minh họa trong tiểu luận, chưa được đóng gói thành thư viện hay ứng dụng độc lập.

## Ý nghĩa trong dạy học

- Trực quan hóa miền nghiệm, nối biểu thức đại số với hình học tọa độ.
- Kiểm chứng kết quả giải toán và thử nhanh ảnh hưởng khi đổi hệ số hoặc dấu bất phương trình.
- Hỗ trợ giáo viên minh họa bài giảng và học sinh tự kiểm tra lời giải.

Công cụ này hỗ trợ tư duy và kiểm chứng, không thay thế lập luận toán học của người học.

## Hướng phát triển

Các hướng khả thi (chưa triển khai):

- Bổ sung kiểm thử tự động và tệp `requirements.txt`.
- Cải thiện thông báo lỗi khi đầu vào sai cú pháp.
- Xử lý đầy đủ các trường hợp suy biến.
- Tách mã nguồn thành các mô-đun.
- Xây dựng giao diện tương tác nếu phù hợp.

## Tác giả và giấy phép

- Nhóm tác giả: sinh viên Trường Đại học Sư phạm Huế. **[CẦN BỔ SUNG]** Họ tên các thành viên.
- Giảng viên hướng dẫn: **[CẦN BỔ SUNG]** theo trang bìa tiểu luận.
- Tài khoản GitHub chủ kho: `duongtam230905-arch`.
- Giấy phép: **[CẦN BỔ SUNG]** Kho chưa có tệp giấy phép.

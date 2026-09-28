"""
====================================================================
 DU AN: "BAN DO VUNG NGHIEM"
 Chu de: He bat phuong trinh bac nhat hai an (Toan 10)
--------------------------------------------------------------------
 giai_he_bpt(): nhan N bat phuong trinh bac nhat hai an duoi dang
 CHUOI (vi du "x + y <= -2", "2*x - y > -1"), tu dong:
   1. Phan tich (parse) tung chuoi bang SymPy -> he so a, b, c va dau.
   2. Tim toan bo dinh cua mien nghiem (giao cac duong bien, loc lai
      nhung diem thoa man TAT CA bat phuong trinh).
   3. Xac dinh mien nghiem la da giac KHEP KIN (bi chan) hay MO RONG
      VO HAN (khong bi chan), bang cach cat mot hinh vuong rat lon
      qua tung nua mat phang (thuat toan Sutherland-Hodgman).
   4. Voi moi canh cua da giac, xac dinh canh do co thuoc duong bien
      cua mot bat phuong trinh NGHIEM NGAT hay khong -> neu co, canh
      do KHONG thuoc mien nghiem (ghi ro trong phan in ra).
   5. In ra he bat phuong trinh, mo ta mien nghiem, kiem tra diem test.

 ve_ban_do(): ve "ban do" theo phong cach toi gian, ro rang:
   - He truc Ox, Oy co mui ten, chi qua goc toa do, KHONG ve khung
     hinh chu nhat, khong ve tick mac dinh.
   - Moi bat phuong trinh co MOT mau/kieu gach rieng (nhat, thua) de
     to phan KHONG phai nghiem; phan nghiem chung de trang.
   - Duong bien: net lien cho <=/>=, net dut cho < / >; nhan phuong
     trinh dat canh duong, nghieng theo dung huong duong do, TU DONG
     di chuyen theo dung vi tri khi nguoi dung zoom/pan.
   - Cac dinh mien nghiem chi ghi chu cai (A, B, C, ...), kem net dut
     vuong goc VE TRON VEN tu truc toi dinh, vach chia nho ngay tren
     truc, va so toa do ghi o PHIA DOI DIEN voi net dut (net dut o
     duoi truc Ox thi so ghi TREN truc Ox; net dut o trai truc Oy thi
     so ghi PHAI truc Oy) - nen KHONG BAO GIO bi net dut de/cham vao.

 Cai dat thu vien can thiet truoc khi chay:
     pip install sympy matplotlib numpy
====================================================================
"""

import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patheffects as pe
import sympy as sp

x, y = sp.symbols('x y', real=True)

# Mau va kieu gach rieng cho tung bat phuong trinh (lap lai neu > 6 bpt)
BANG_MAU = ['#2ecc71', '#e74c3c', '#3498db', '#9b59b6', '#f39c12', '#1abc9c']
BANG_GACH = ['/', '\\', 'x', '.', '+', 'o']   # 1 ky tu -> gach thua, nhat hon

SAI_SO = 1e-7
L_HOP_LON = 1.0e5

mpl.rcParams['hatch.linewidth'] = 0.6  # net gach mong, do bot roi mat


# ====================================================================
# PHAN 1: PHAN TICH CHUOI BAT PHUONG TRINH
# ====================================================================
def phan_tich_bpt(chuoi):
    bieu_thuc = sp.sympify(chuoi, locals={'x': x, 'y': y})
    if not isinstance(bieu_thuc, sp.core.relational.Relational):
        raise ValueError(f"'{chuoi}' khong phai la mot bat phuong trinh hop le.")
    dau = bieu_thuc.rel_op
    if dau == '==':
        raise ValueError(f"'{chuoi}' la phuong trinh (=), ham nay chi nhan bat phuong trinh.")

    hieu = sp.expand(bieu_thuc.lhs - bieu_thuc.rhs)
    a = float(hieu.coeff(x))
    b = float(hieu.coeff(y))
    d = float(hieu.subs({x: 0, y: 0}))
    c = -d

    if abs(a) < SAI_SO and abs(b) < SAI_SO:
        raise ValueError(f"'{chuoi}' khong chua x hoac y voi he so khac 0.")

    return {'a': a, 'b': b, 'c': c, 'op': dau, 'chuoi_goc': chuoi.strip()}


def chuoi_phuong_trinh_duong(bpt):
    """Chuoi hien thi phuong trinh duong bien, vi du 'x + y = -2'."""
    a, b, c = bpt['a'], bpt['b'], bpt['c']

    def he_so(v, ten, dau_dau):
        if abs(v) < SAI_SO:
            return ""
        so = lam_dep_so(abs(v))
        so = "" if so == "1" else so
        dau = ("" if dau_dau else (" + " if v > 0 else " - ")) if not dau_dau else ("-" if v < 0 else "")
        return f"{dau}{so}{ten}"

    phan_x = he_so(a, "x", True)
    phan_y = he_so(b, "y", False)
    ve_trai = (phan_x + phan_y).strip()
    if ve_trai.startswith("+"):
        ve_trai = ve_trai[1:].strip()
    return f"{ve_trai} = {lam_dep_so(c)}"


# ====================================================================
# PHAN 2: KIEM TRA DIEM VOI BAT PHUONG TRINH
# ====================================================================
def thoa_man_dong(bpt, px, py):
    gt = bpt['a'] * px + bpt['b'] * py
    if bpt['op'] in ('<=', '<'):
        return gt <= bpt['c'] + SAI_SO
    else:
        return gt >= bpt['c'] - SAI_SO


def thoa_man_thuc(bpt, px, py):
    gt = bpt['a'] * px + bpt['b'] * py
    if bpt['op'] == '<=':
        return gt <= bpt['c'] + SAI_SO
    if bpt['op'] == '>=':
        return gt >= bpt['c'] - SAI_SO
    if bpt['op'] == '<':
        return gt < bpt['c'] - SAI_SO
    if bpt['op'] == '>':
        return gt > bpt['c'] + SAI_SO
    raise ValueError("Dau khong hop le")


def diem_thuoc_mien_nghiem(danh_sach_bpt, px, py):
    return all(thoa_man_thuc(bpt, px, py) for bpt in danh_sach_bpt)


def diem_nam_tren_duong(bpt, px, py, tol=1e-4):
    return abs(bpt['a'] * px + bpt['b'] * py - bpt['c']) < tol


# ====================================================================
# PHAN 3: TIM DINH MIEN NGHIEM
# ====================================================================
def giao_diem_hai_duong(bpt_i, bpt_j):
    A = np.array([[bpt_i['a'], bpt_i['b']],
                  [bpt_j['a'], bpt_j['b']]])
    C = np.array([bpt_i['c'], bpt_j['c']])
    dinh_thuc = np.linalg.det(A)
    if abs(dinh_thuc) < SAI_SO:
        return None
    px, py = np.linalg.solve(A, C)
    return (float(px), float(py))


def tim_dinh_mien_nghiem(danh_sach_bpt):
    ung_vien = []
    for bpt_i, bpt_j in itertools.combinations(danh_sach_bpt, 2):
        giao = giao_diem_hai_duong(bpt_i, bpt_j)
        if giao is None:
            continue
        px, py = giao
        if all(thoa_man_dong(bpt, px, py) for bpt in danh_sach_bpt):
            ung_vien.append((px, py))

    dinh_duy_nhat = []
    for p in ung_vien:
        if not any(abs(p[0] - q[0]) < 1e-5 and abs(p[1] - q[1]) < 1e-5 for q in dinh_duy_nhat):
            dinh_duy_nhat.append(p)
    return dinh_duy_nhat


def sap_xep_nguoc_kim_dong_ho(danh_sach_diem):
    if len(danh_sach_diem) < 3:
        return danh_sach_diem
    cx = sum(p[0] for p in danh_sach_diem) / len(danh_sach_diem)
    cy = sum(p[1] for p in danh_sach_diem) / len(danh_sach_diem)
    return sorted(danh_sach_diem, key=lambda p: np.arctan2(p[1] - cy, p[0] - cx))


def tim_bpt_chung(v1, v2, danh_sach_bpt):
    """Tim bat phuong trinh ma duong bien di qua CA HAI dinh v1, v2 (canh nam tren duong nay)."""
    ung_vien = [bpt for bpt in danh_sach_bpt
                if diem_nam_tren_duong(bpt, *v1) and diem_nam_tren_duong(bpt, *v2)]
    return ung_vien[0] if ung_vien else None


# ====================================================================
# PHAN 4: BI CHAN / KHONG BI CHAN (cat hinh vuong lon)
# ====================================================================
def cat_doan_thang_qua_duong(p1, p2, bpt):
    x1, y1 = p1
    x2, y2 = p2
    a, b, c = bpt['a'], bpt['b'], bpt['c']
    mau_so = a * (x2 - x1) + b * (y2 - y1)
    if abs(mau_so) < 1e-12:
        return p2
    t = (c - a * x1 - b * y1) / mau_so
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def cat_da_giac_boi_bpt(da_giac, bpt):
    if not da_giac:
        return []
    ket_qua = []
    n = len(da_giac)
    for i in range(n):
        hien_tai = da_giac[i]
        ke_tiep = da_giac[(i + 1) % n]
        trong_hien_tai = thoa_man_dong(bpt, *hien_tai)
        trong_ke_tiep = thoa_man_dong(bpt, *ke_tiep)
        if trong_hien_tai:
            ket_qua.append(hien_tai)
            if not trong_ke_tiep:
                ket_qua.append(cat_doan_thang_qua_duong(hien_tai, ke_tiep, bpt))
        else:
            if trong_ke_tiep:
                ket_qua.append(cat_doan_thang_qua_duong(hien_tai, ke_tiep, bpt))
    return ket_qua


def cat_hop_lon_boi_tat_ca_bpt(danh_sach_bpt, L=L_HOP_LON):
    da_giac = [(-L, -L), (L, -L), (L, L), (-L, L)]
    for bpt in danh_sach_bpt:
        da_giac = cat_da_giac_boi_bpt(da_giac, bpt)
        if not da_giac:
            break
    return da_giac


def diem_o_bien_hop_lon(p, L=L_HOP_LON):
    return abs(abs(p[0]) - L) < 1e-3 or abs(abs(p[1]) - L) < 1e-3


def lam_dep_so(v):
    if abs(v - round(v)) < 1e-6:
        return str(int(round(v)))
    return str(round(v, 4))


# ====================================================================
# PHAN 5: MO TA MIEN NGHIEM
# ====================================================================
def mo_ta_mien_nghiem(danh_sach_bpt):
    dinh_that = tim_dinh_mien_nghiem(danh_sach_bpt)
    da_giac_cat = cat_hop_lon_boi_tat_ca_bpt(danh_sach_bpt)
    ten_chu_cai = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    if not da_giac_cat:
        print("  => He VO NGHIEM (khong ton tai diem nao thoa man dong thoi tat ca bat phuong trinh).")
        return {'loai': 'vo_nghiem', 'dinh': [], 'ten_dinh': {}, 'canh_mo': []}

    bi_chan = not any(diem_o_bien_hop_lon(p) for p in da_giac_cat)

    if bi_chan:
        dinh_sx = sap_xep_nguoc_kim_dong_ho(dinh_that)
        n = len(dinh_sx)
        ten_dinh = {}
        for i, (px, py) in enumerate(dinh_sx):
            ten_dinh[(round(px, 6), round(py, 6))] = ten_chu_cai[i % 26]

        ten_list = [ten_dinh[(round(px, 6), round(py, 6))] for (px, py) in dinh_sx]

        canh_mo = []  # danh sach (ten_a, ten_b, bpt) cac canh KHONG thuoc mien nghiem
        for i in range(n):
            v1, v2 = dinh_sx[i], dinh_sx[(i + 1) % n]
            bpt_chung = tim_bpt_chung(v1, v2, danh_sach_bpt)
            if bpt_chung is not None and bpt_chung['op'] in ('<', '>'):
                ta, tb = ten_dinh[(round(v1[0], 6), round(v1[1], 6))], ten_dinh[(round(v2[0], 6), round(v2[1], 6))]
                canh_mo.append((ta, tb, bpt_chung))

        ten_dinh_str = ", ".join(f"{c}({lam_dep_so(px)}, {lam_dep_so(py)})" for (px, py), c in
                                  ((p, ten_dinh[(round(p[0], 6), round(p[1], 6))]) for p in dinh_sx))
        if canh_mo:
            phan_khong_tinh = ", ".join(f"{ta}{tb}" for ta, tb, _ in canh_mo)
            tu_canh = "canh" if len(canh_mo) == 1 else "cac canh"
            print(f"  => Mien nghiem cua he bat phuong trinh tren la da giac {''.join(ten_list)} "
                  f"(khong tinh {tu_canh} {phan_khong_tinh}), voi {ten_dinh_str}.")
        else:
            print(f"  => Mien nghiem cua he bat phuong trinh tren la da giac {''.join(ten_list)}, "
                  f"voi {ten_dinh_str}.")

        return {'loai': 'bi_chan', 'dinh': dinh_sx, 'ten_dinh': ten_dinh, 'canh_mo': canh_mo}

    else:
        def la_dinh_that(p):
            for q in dinh_that:
                if abs(p[0] - q[0]) < 1e-3 and abs(p[1] - q[1]) < 1e-3:
                    return q
            return None

        n = len(da_giac_cat)
        nhan_diem = []
        for p in da_giac_cat:
            dt = la_dinh_that(p)
            nhan_diem.append((dt, 'that') if dt is not None else (p, 'nhan_tao'))

        print("  => Mien nghiem KHONG BI CHAN (mo rong vo han). Cac dinh thuc su tinh duoc:")
        ten_dinh = {}
        dem = 0
        for p, loai in nhan_diem:
            if loai == 'that':
                c = ten_chu_cai[dem % 26]
                ten_dinh[(round(p[0], 6), round(p[1], 6))] = c
                print(f"       {c}({lam_dep_so(p[0])}, {lam_dep_so(p[1])})")
                dem += 1
        if dem == 0:
            print("       (khong co dinh huu han nao)")

        canh_mo = []
        print("     Cac canh/tia vo han cua mien nghiem:")
        for i in range(n):
            p_hien_tai, loai_hien_tai = nhan_diem[i]
            p_ke, loai_ke = nhan_diem[(i + 1) % n]
            if loai_hien_tai == 'that' and loai_ke == 'nhan_tao':
                huong = (p_ke[0] - p_hien_tai[0], p_ke[1] - p_hien_tai[1])
                do_lon = np.hypot(*huong)
                hd = (huong[0] / do_lon, huong[1] / do_lon) if do_lon > 0 else (0, 0)
                ten_c = ten_dinh[(round(p_hien_tai[0], 6), round(p_hien_tai[1], 6))]
                print(f"       - Tia xuat phat tu {ten_c}, keo dai vo tan theo huong ({lam_dep_so(hd[0])}, {lam_dep_so(hd[1])})")
            elif loai_hien_tai == 'nhan_tao' and loai_ke == 'that':
                huong = (p_hien_tai[0] - p_ke[0], p_hien_tai[1] - p_ke[1])
                do_lon = np.hypot(*huong)
                hd = (huong[0] / do_lon, huong[1] / do_lon) if do_lon > 0 else (0, 0)
                ten_c = ten_dinh[(round(p_ke[0], 6), round(p_ke[1], 6))]
                print(f"       - Tia xuat phat tu {ten_c}, keo dai vo tan theo huong ({lam_dep_so(hd[0])}, {lam_dep_so(hd[1])})")
            elif loai_hien_tai == 'that' and loai_ke == 'that':
                ten_a = ten_dinh[(round(p_hien_tai[0], 6), round(p_hien_tai[1], 6))]
                ten_b = ten_dinh[(round(p_ke[0], 6), round(p_ke[1], 6))]
                bpt_chung = tim_bpt_chung(p_hien_tai, p_ke, danh_sach_bpt)
                ghi_chu = ""
                if bpt_chung is not None and bpt_chung['op'] in ('<', '>'):
                    canh_mo.append((ten_a, ten_b, bpt_chung))
                    ghi_chu = f"  (khong tinh canh {ten_a}{ten_b})"
                print(f"       - Canh huu han noi {ten_a} - {ten_b}{ghi_chu}")

        return {'loai': 'khong_bi_chan', 'dinh': dinh_that, 'ten_dinh': ten_dinh, 'canh_mo': canh_mo}


# ====================================================================
# PHAN 6: HAM TONG QUAT
# ====================================================================
def giai_he_bpt(danh_sach_chuoi, diem_test=None):
    danh_sach_bpt = [phan_tich_bpt(s) for s in danh_sach_chuoi]

    print("=" * 70)
    print("HE BAT PHUONG TRINH BAC NHAT HAI AN:")
    for i, bpt in enumerate(danh_sach_bpt, start=1):
        print(f"  d{i}:  {bpt['chuoi_goc']}")

    print("\nMIEN NGHIEM:")
    mo_ta = mo_ta_mien_nghiem(danh_sach_bpt)

    if diem_test:
        print("\nKIEM TRA CAC DIEM TEST:")
        for (x0, y0) in diem_test:
            thuoc = diem_thuoc_mien_nghiem(danh_sach_bpt, x0, y0)
            if thuoc:
                print(f"  Diem ({lam_dep_so(x0)}, {lam_dep_so(y0)}): THUOC mien nghiem")
            else:
                vi_pham = [f"d{i+1}" for i, bpt in enumerate(danh_sach_bpt) if not thoa_man_thuc(bpt, x0, y0)]
                print(f"  Diem ({lam_dep_so(x0)}, {lam_dep_so(y0)}): KHONG thuoc mien nghiem (vi pham: {', '.join(vi_pham)})")
    print("=" * 70)
    return danh_sach_bpt, mo_ta


# ====================================================================
# PHAN 7: VE BAN DO
# ====================================================================
def hai_diem_tren_duong(bpt, x_lo, x_hi, y_lo, y_hi):
    a, b, c = bpt['a'], bpt['b'], bpt['c']
    if abs(b) > SAI_SO:
        return (x_lo, (c - a * x_lo) / b), (x_hi, (c - a * x_hi) / b)
    else:
        return (c / a, y_lo), (c / a, y_hi)


def ve_ban_do(danh_sach_bpt, mo_ta, diem_test=None, xlim=(-6, 6), ylim=(-6, 6)):
    diem_test = diem_test or []
    fig, ax = plt.subplots(figsize=(9.5, 9.5))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

    # An khung hinh chu nhat + tick mac dinh: chi giu truc Ox, Oy tu ve
    for canh in ('top', 'right', 'left', 'bottom'):
        ax.spines[canh].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal', adjustable='box')

    doi_tuong_dong = {'gach': [], 'truc': [], 'nhan_duong': []}

    def xoa_nhom(ten):
        for obj in doi_tuong_dong[ten]:
            try:
                obj.remove()
            except Exception:
                for coll in getattr(obj, 'collections', []):
                    try:
                        coll.remove()
                    except Exception:
                        pass
        doi_tuong_dong[ten] = []

    # ---- Ve lai phan gach/to mau (nhat, thua) theo vung nhin hien tai ----
    def ve_lai_gach(so_diem_luoi=320):
        xoa_nhom('gach')
        x_lo, x_hi = ax.get_xlim()
        y_lo, y_hi = ax.get_ylim()
        xs = np.linspace(x_lo, x_hi, so_diem_luoi)
        ys = np.linspace(y_lo, y_hi, so_diem_luoi)
        X, Y = np.meshgrid(xs, ys)
        for i, bpt in enumerate(danh_sach_bpt):
            gt = bpt['a'] * X + bpt['b'] * Y
            if bpt['op'] == '<=':
                thoa = gt <= bpt['c']
            elif bpt['op'] == '>=':
                thoa = gt >= bpt['c']
            elif bpt['op'] == '<':
                thoa = gt < bpt['c']
            else:
                thoa = gt > bpt['c']
            nhan = np.where(thoa, 1, 0)
            mau = BANG_MAU[i % len(BANG_MAU)]
            gach = BANG_GACH[i % len(BANG_GACH)]
            to_mau = ax.contourf(X, Y, nhan, levels=[-0.5, 0.5], colors=[mau], alpha=0.16, zorder=1)
            gach_cheo = ax.contourf(X, Y, nhan, levels=[-0.5, 0.5], colors=['none'], hatches=[gach], zorder=1)
            doi_tuong_dong['gach'].extend([to_mau, gach_cheo])

    # ---- Ve lai truc Ox, Oy co mui ten (luon cham toi mep khung nhin) ----
    def ve_lai_truc():
        xoa_nhom('truc')
        x_lo, x_hi = ax.get_xlim()
        y_lo, y_hi = ax.get_ylim()
        duong_x = ax.annotate('', xy=(x_hi, 0), xytext=(x_lo, 0),
                               arrowprops=dict(arrowstyle='-|>', color='black', lw=1.3,
                                                shrinkA=0, shrinkB=0), zorder=4)
        duong_y = ax.annotate('', xy=(0, y_hi), xytext=(0, y_lo),
                               arrowprops=dict(arrowstyle='-|>', color='black', lw=1.3,
                                                shrinkA=0, shrinkB=0), zorder=4)
        nhan_x = ax.text(x_hi, 0, '  x', fontsize=13, style='italic', ha='left', va='center', zorder=4)
        nhan_y = ax.text(0, y_hi, 'y  ', fontsize=13, style='italic', ha='center', va='bottom', zorder=4)
        nhan_o = ax.text(-0.02 * (x_hi - x_lo), -0.02 * (y_hi - y_lo), 'O',
                          fontsize=12, ha='right', va='top', zorder=4)
        doi_tuong_dong['truc'] = [duong_x, duong_y, nhan_x, nhan_y, nhan_o]

    # ---- Ve lai nhan phuong trinh duong - tu dich chuyen khi zoom ----
    def ve_lai_nhan_duong():
        xoa_nhom('nhan_duong')
        x_lo, x_hi = ax.get_xlim()
        y_lo, y_hi = ax.get_ylim()
        bien_x = 0.06 * (x_hi - x_lo)
        bien_y = 0.06 * (y_hi - y_lo)
        cac_ti_le = [0.78, 0.65, 0.5, 0.35, 0.2, 0.88, 0.12]
        for i, bpt in enumerate(danh_sach_bpt):
            mau = BANG_MAU[i % len(BANG_MAU)]
            a, b, c = bpt['a'], bpt['b'], bpt['c']
            vi_tri = None

            if abs(b) > SAI_SO:
                for f in cac_ti_le:
                    xt = x_lo + f * (x_hi - x_lo)
                    yt = (c - a * xt) / b
                    if y_lo + bien_y <= yt <= y_hi - bien_y:
                        vi_tri = (xt, yt)
                        break
            if vi_tri is None and abs(a) > SAI_SO:
                for f in cac_ti_le:
                    yt = y_lo + f * (y_hi - y_lo)
                    xt = (c - b * yt) / a
                    if x_lo + bien_x <= xt <= x_hi - bien_x:
                        vi_tri = (xt, yt)
                        break
            if vi_tri is None:
                xt = c / a
                for f in cac_ti_le:
                    yt = y_lo + f * (y_hi - y_lo)
                    if x_lo + bien_x <= xt <= x_hi - bien_x:
                        vi_tri = (xt, yt)
                        break
            if vi_tri is None:
                vi_tri = (x_lo + 0.5 * (x_hi - x_lo), y_lo + 0.5 * (y_hi - y_lo))

            x_nhan, y_nhan = vi_tri
            noi_dung = chuoi_phuong_trinh_duong(bpt)

            do_dai_huong = np.hypot(b, a)
            hx, hy = (-b / do_dai_huong, a / do_dai_huong) if do_dai_huong > 0 else (1, 0)
            eps = 0.01 * (x_hi - x_lo)
            p_a = ax.transData.transform((x_nhan - eps * hx, y_nhan - eps * hy))
            p_b = ax.transData.transform((x_nhan + eps * hx, y_nhan + eps * hy))
            goc = np.degrees(np.arctan2(p_b[1] - p_a[1], p_b[0] - p_a[0]))
            if goc > 90:
                goc -= 180
            elif goc < -90:
                goc += 180

            do_dai_phap = np.hypot(a, b)
            nx, ny = (a / do_dai_phap, b / do_dai_phap) if do_dai_phap > 0 else (0, 1)
            do_lech = 0.018 * min(x_hi - x_lo, y_hi - y_lo)

            nhan = ax.text(x_nhan + nx * do_lech, y_nhan + ny * do_lech, noi_dung,
                            fontsize=12, fontweight='bold', fontstyle='italic',
                            color=mau, ha='center', va='center', zorder=6,
                            rotation=goc, rotation_mode='anchor',
                            path_effects=[pe.withStroke(linewidth=3, foreground='white')])
            doi_tuong_dong['nhan_duong'].append(nhan)

    def ve_lai_tat_ca(event=None):
        ve_lai_gach()
        ve_lai_truc()
        ve_lai_nhan_duong()
        fig.canvas.draw_idle()

    ve_lai_tat_ca()
    ax.callbacks.connect('xlim_changed', ve_lai_tat_ca)
    ax.callbacks.connect('ylim_changed', ve_lai_tat_ca)

    # ---- Ve duong bien (net lien / net dut) ----
    for i, bpt in enumerate(danh_sach_bpt):
        mau = BANG_MAU[i % len(BANG_MAU)]
        net = '-' if bpt['op'] in ('<=', '>=') else '--'
        p1, p2 = hai_diem_tren_duong(bpt, *xlim, *ylim)
        ax.axline(p1, p2, color=mau, linewidth=2.0, linestyle=net, zorder=3)

    # ---- Danh dau dinh: chi ghi chu cai + net dut vuong goc (VE TRON VEN,
    # KHONG cat) + vach nho + so ghi o PHIA DOI DIEN voi net dut, nen khong
    # bao gio bi net dut de len ----
    TICK_Y = 0.014 * (ylim[1] - ylim[0])
    TICK_X = 0.014 * (xlim[1] - xlim[0])
    KHOANG_SO_Y = 11   # diem anh (points), khoang cach tu truc Ox toi so
    KHOANG_SO_X = 10   # diem anh (points), khoang cach tu truc Oy toi so

    for (px, py) in mo_ta.get('dinh', []):
        ten = mo_ta.get('ten_dinh', {}).get((round(px, 6), round(py, 6)), '')
        ax.scatter(px, py, s=70, color='black', zorder=7)
        ax.annotate(ten, (px, py), textcoords="offset points", xytext=(12, 12),
                    fontsize=13, fontweight='bold', zorder=7)

        # net dut vuong goc xuong Ox va sang Oy - ve TRON VEN tu truc toi dinh
        ax.plot([px, px], [0, py], linestyle=(0, (5, 3)), color='black',
                 linewidth=1.4, alpha=0.85, zorder=2)
        ax.plot([0, px], [py, py], linestyle=(0, (5, 3)), color='black',
                 linewidth=1.4, alpha=0.85, zorder=2)

        # vach nho ngay tren truc (giong vach chia do) tai dung vi tri gia tri
        ax.plot([px, px], [-TICK_Y, TICK_Y], color='black', linewidth=2.2, zorder=6)
        ax.plot([-TICK_X, TICK_X], [py, py], color='black', linewidth=2.2, zorder=6)

        # So ghi o PHIA DOI DIEN voi net dut (net dut o duoi truc Ox thi so
        # ghi TREN truc Ox; net dut o ben trai truc Oy thi so ghi BEN PHAI
        # truc Oy) - nho vay so va net dut khong bao gio de/cham vao nhau
        if py <= 0:
            ax.annotate(lam_dep_so(px), xy=(px, 0), xycoords='data',
                        xytext=(0, KHOANG_SO_Y), textcoords='offset points',
                        ha='center', va='bottom', fontsize=13, fontweight='bold', zorder=6)
        else:
            ax.annotate(lam_dep_so(px), xy=(px, 0), xycoords='data',
                        xytext=(0, -KHOANG_SO_Y), textcoords='offset points',
                        ha='center', va='top', fontsize=13, fontweight='bold', zorder=6)

        if px <= 0:
            ax.annotate(lam_dep_so(py), xy=(0, py), xycoords='data',
                        xytext=(KHOANG_SO_X, 0), textcoords='offset points',
                        ha='left', va='center', fontsize=13, fontweight='bold', zorder=6)
        else:
            ax.annotate(lam_dep_so(py), xy=(0, py), xycoords='data',
                        xytext=(-KHOANG_SO_X, 0), textcoords='offset points',
                        ha='right', va='center', fontsize=13, fontweight='bold', zorder=6)

    # ---- Diem test ----
    for (x0, y0) in diem_test:
        thuoc = diem_thuoc_mien_nghiem(danh_sach_bpt, x0, y0)
        mau_diem = 'green' if thuoc else 'red'
        ky_hieu = 'o' if thuoc else 'X'
        ax.scatter(x0, y0, s=140, color=mau_diem, marker=ky_hieu,
                   edgecolor='black', linewidth=1.1, zorder=8)
        ax.annotate(f"({lam_dep_so(x0)},{lam_dep_so(y0)})", (x0, y0),
                    textcoords="offset points", xytext=(10, -12),
                    fontsize=9, fontweight='bold', color=mau_diem, zorder=8)

    ax.set_title('BAN DO VUNG NGHIEM', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.show()


# ====================================================================
# DEMO
# ====================================================================
if __name__ == "__main__":
    he_bpt_chuoi = [
        "x + y <= 2",     # d1 - net lien
        "x - y < 3",       # d2 - NGHIEM NGAT -> net dut
        "2*x - y >= 1",   # d3 - net lien
    ]
    # Mien nghiem la tam giac A(-2,-3) B(-0.5,-1.5) C(-1,-1); canh AB nam
    # tren duong d2 (nghiem ngat) nen KHONG thuoc mien nghiem.

    diem_can_test = [(-1.5, -2), (-3, -3)]

    danh_sach_bpt, mo_ta = giai_he_bpt(he_bpt_chuoi, diem_test=diem_can_test)
    ve_ban_do(danh_sach_bpt, mo_ta, diem_test=diem_can_test, xlim=(-5, 3), ylim=(-5, 3))
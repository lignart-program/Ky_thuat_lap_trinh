import os
from datetime import datetime
import sys

# HÀM TẠO FILE .bat CHẠY CHƯƠNG TRÌNH NGOÀI VSCODE
def taoFileKhoiDong():
    BatFile="ChayPhanMem.bat"
    if not os.path.exists(BatFile):
        TenFile=os.path.basename(sys.argv[0])
        with open(BatFile, 'w', encoding='utf-8') as F:
            F.write("@echo off\n")
            F.write("chcp 65001 > nul\n")
            F.write('cd /d "%~dp0"\n')
            F.write("title Hệ Thống Quản Lý Dự Án\n")
            F.write("color F0\n") 
            F.write("echo Đang khởi động hệ thống...\n")
            F.write(f'python "{TenFile}"\n')
            F.write("pause\n")
        print(f"[*] Hệ thống đã tự động tạo file launcher: '{BatFile}'")
        print("[*] Click đúp vào file này để mở trực tiếp phần mềm!\n")

# 1. CẤU TRÚC DỮ LIỆU DANH SÁCH LIÊN KẾT ĐƠN
class Nut:
    def __init__(self, Data):
        self.Data=Data
        self.Next=None

class DanhSachMocNoi:
    def __init__(self):
        self.Head=None
        self.Length=0
        
    def themPT(self, Data):
        NewNode=Nut(Data)
        if not self.Head:
            self.Head=NewNode
        else:
            NutHT=self.Head
            while NutHT.Next:
                NutHT=NutHT.Next
            NutHT.Next=NewNode
        self.Length+=1
        
    def __iter__(self):
        NutHT=self.Head
        while NutHT:
            yield NutHT.Data
            NutHT=NutHT.Next
            
    def __len__(self):
        return self.Length
        
    def get(self, Index):
        NutHT=self.Head
        Count=0
        while NutHT:
            if Count == Index:
                return NutHT.Data
            Count+=1
            NutHT=NutHT.Next
        return None

def ngatChuoi(Str, DauPhanCach): 
    KetQua=DanhSachMocNoi()
    K=""
    for Char in Str:
        if Char == DauPhanCach:
            KetQua.themPT(K)
            K=""
        else:
            K+=Char
    KetQua.themPT(K)
    return KetQua

# 2. ĐỊNH NGHĨA CÁC LỚP ĐỐI TƯỢNG 
class ThanhVien:
    def __init__(self, Ten, VaiTro, DonGia):
        self.Ten=Ten
        self.VaiTro=VaiTro
        self.DonGia=float(DonGia)

class CongViec:
    def __init__(self, MaCV, TenCV, LoaiHinh, CongViecYeuCau="", TrangThai="To Do"):
        self.MaCV=MaCV
        self.TenCV=TenCV
        self.LoaiHinh=LoaiHinh
        self.CongViecYeuCau=CongViecYeuCau
        self.TrangThai=TrangThai

class NhatKyChamCong:
    def __init__(self, MaCV, NguoiThucHien, NgayChamCong, SoGioLam):
        self.MaCV=MaCV
        self.NguoiThucHien=NguoiThucHien
        self.NgayChamCong=NgayChamCong
        self.SoGioLam=float(SoGioLam)

class DuAn:
    def __init__(self, MaDA, TenDA, KhachHang, NganSach, TgBatDau, TgKetThuc):
        self.MaDA=MaDA
        self.TenDA=TenDA
        self.KhachHang=KhachHang
        self.NganSach=float(NganSach)
        self.TgBatDau=TgBatDau
        self.TgKetThuc=TgKetThuc

        self.ThanhVien=DanhSachMocNoi()      
        self.DanhMucCV=DanhSachMocNoi()    
        self.NhatKyCong=DanhSachMocNoi()  

# 3. QUẢN LÝ LƯU TRỮ VÀ ĐỌC FILE
FileName="du_an_database.txt"
def luuDuLieu(Projects):
    with open(FileName, 'w', encoding='utf-8') as F:
        for P in Projects:
            F.write(f"PROJECT|{P.MaDA}|{P.TenDA}|{P.KhachHang}|{P.NganSach}|{P.TgBatDau}|{P.TgKetThuc}\n")
            for Tv in P.ThanhVien:
                F.write(f"MEMBER|{Tv.Ten}|{Tv.VaiTro}|{Tv.DonGia}\n")
            for Cv in P.DanhMucCV:
                F.write(f"TASK_CATALOG|{Cv.MaCV}|{Cv.TenCV}|{Cv.LoaiHinh}|{Cv.CongViecYeuCau}|{Cv.TrangThai}\n")
            for Nk in P.NhatKyCong:
                F.write(f"TIMESHEET|{Nk.MaCV}|{Nk.NguoiThucHien}|{Nk.NgayChamCong}|{Nk.SoGioLam}\n")

def capNhatDuLieu():
    Projects=DanhSachMocNoi()
    if not os.path.exists(FileName):
        return Projects
    ProjectHT=None
    with open(FileName, 'r', encoding='utf-8') as F:
        for L in F:
            try: 
                L=L.strip()
                if not L:
                    continue
                P=ngatChuoi(L, "|")   
                T=P.get(0)
                if T == "PROJECT":
                    ProjectHT=DuAn(P.get(1), P.get(2), P.get(3), P.get(4), P.get(5), P.get(6))
                    Projects.themPT(ProjectHT)
                elif T == "MEMBER" and ProjectHT:
                    ChuoiDonGia=str(P.get(3) or "0").replace('.', '').replace(',', '')
                    Tv=ThanhVien(P.get(1), P.get(2), float(ChuoiDonGia))
                    ProjectHT.ThanhVien.themPT(Tv)
                elif T == "TASK_CATALOG" and ProjectHT:
                    Val4=P.get(4)
                    Val5=P.get(5)
                    if Val5 is not None:
                        YeuCau=Val4
                        TrangThai=Val5
                    else:
                        YeuCau=""
                        TrangThai=Val4 if Val4 else "To Do"
                    Cv=CongViec(P.get(1), P.get(2), P.get(3), YeuCau, TrangThai)
                    ProjectHT.DanhMucCV.themPT(Cv)
                elif T == "TIMESHEET" and ProjectHT:
                    Nk=NhatKyChamCong(P.get(1), P.get(2), P.get(3), P.get(4))
                    ProjectHT.NhatKyCong.themPT(Nk)
            except Exception:
                print(f"[*] Cảnh báo: Bỏ qua 1 dòng dữ liệu bị hỏng trong file database.")
                continue
    return Projects     

# 4. LOGIC XỬ LÝ CHỨC NĂNG NGHIỆP VỤ VÀ XÁC NHẬN
def timDA(Projects, MaDA):
    for P in Projects:
        if P.MaDA == MaDA:
            return P
    return None

def timThanhVien(Project, TenNguoi):
    for Tv in Project.ThanhVien:
        if Tv.Ten == TenNguoi:
            return Tv
    return None

def timCV(Project, MaCV):
    for Cv in Project.DanhMucCV:
        if Cv.MaCV == MaCV:
            return Cv
    return None

def nhapVaTimDuAn(Projects):
    while True:
        MaDA=input("\nNhập mã dự án (hoặc '0' để quay lại menu): ").strip()
        if MaDA == '0':
            return None
        if not MaDA:
            print("Lỗi: Mã dự án không được để trống!")
            continue
            
        P=timDA(Projects, MaDA)
        if P:
            return P    
        else:
            print("Lỗi: Không tìm thấy dự án! Vui lòng kiểm tra lại mã.")

def nhapNgay(ThongDiep):
    while True:
        NgayStr=input(ThongDiep).strip()
        try:
            NgayHopLe=datetime.strptime(NgayStr, "%d/%m/%Y")
            return NgayHopLe
        except ValueError:
            print("Lỗi: Định dạng ngày không hợp lệ! Vui lòng nhập theo chuẩn DD/MM/YYYY (VD: 20/06/2026).")

def taoDuAn(Projects):
    print("\n--- TẠO DỰ ÁN MỚI ---")
    while True:
        MaDA=input("Mã dự án (VD: DA01): ").strip()
        if MaDA:
            if timDA(Projects, MaDA):
                print("Lỗi: Mã dự án đã tồn tại!")
            else:
                break
        else:
            print("Lỗi: Không được để trống mã dự án!")

    while True:
        TenDA=input("Tên dự án: ").strip().replace('|', '-')
        if TenDA:
            break
        print("Lỗi: Tên dự án không được để trống!")
        
    KhachHang=input("Tên khách hàng: ").strip().replace('|', '-')
    
    while True:
        ChuoiNganSach=input("Ngân sách (VND): ").strip().replace('.', '').replace(',', '')
        try:
            NganSach=float(ChuoiNganSach)
            if NganSach <= 0:
                print("Lỗi: Ngân sách phải lớn hơn 0!")
                continue
            break
        except ValueError:
            print("Lỗi: Ngân sách không hợp lệ! Vui lòng nhập số.")

    print("\n-- THỜI GIAN TRIỂN KHAI --")
    while True:
        TgBatDauObj=nhapNgay("Ngày bắt đầu (DD/MM/YYYY): ")
        TgKetThucObj=nhapNgay("Ngày kết thúc (DD/MM/YYYY): ")
        
        if TgKetThucObj >= TgBatDauObj:
            break
        else:
            print("Lỗi: Ngày kết thúc không thể diễn ra trước ngày bắt đầu! Vui lòng nhập lại.")
    TgBatDau=TgBatDauObj.strftime("%d/%m/%Y")
    TgKetThuc=TgKetThucObj.strftime("%d/%m/%Y")

    NewP=DuAn(MaDA, TenDA, KhachHang, NganSach, TgBatDau, TgKetThuc)
    Projects.themPT(NewP)
    print("-> Đã thêm dự án thành công!")

def themThanhVien(Projects):
    print("\n--- THÊM THÀNH VIÊN VÀO DỰ ÁN ---")
    P=nhapVaTimDuAn(Projects)
    if not P:
        return
    print("1. Nhập từ file CSV | 2. Nhập tay")
    Chon=input("Lựa chọn (1/2): ").strip()

    if Chon == "1":
        FileExcel=input("Nhập tên file nhân sự (VD: nhan_su.csv): ").strip()
        if not os.path.exists(FileExcel):
            print("Lỗi: Không tìm thấy file!")
            return
        SoLuong=0
        DongDau=True 
        with open(FileExcel, 'r', encoding='utf-8') as F:
            for L in F:
                L=L.strip()
                if not L:
                    continue
                if DongDau:
                    DongDau=False 
                    continue 
                K=ngatChuoi(L, ",")
                if len(K) >= 3:
                    Ten=K.get(0).strip().replace('|', '-')
                    VaiTro=K.get(1).strip().replace('|', '-')
                    
                    if timThanhVien(P, Ten):
                        print(f" ! Bỏ qua: Nhân sự '{Ten}' đã tồn tại trong dự án.")
                        continue
                        
                    try:
                        ChuoiDonGia=K.get(2).strip().replace('.', '').replace(',', '')
                        DonGia=float(ChuoiDonGia)
                        P.ThanhVien.themPT(ThanhVien(Ten, VaiTro, DonGia))
                        SoLuong+=1
                        print(f" + Nạp thành công: {Ten} - {DonGia:,.0f} VND")
                    except ValueError:
                        print(f" -> Lỗi đơn giá của '{Ten}'. Bỏ qua.")
        print(f"-> Hoàn tất: Đã nạp {SoLuong} nhân sự.")
    elif Chon == "2":
        print("Nhập thông tin nhân sự. Nhập '0' tại mục Tên để hoàn tất.")
        while True:
            Ten=input("\nTên (hoặc '0' để thoát): ").strip().replace('|', '-')
            if Ten == '0' or Ten == '':
                break        
            if timThanhVien(P, Ten):
                print("Lỗi: Nhân sự này đã tồn tại! Vui lòng nhập thêm hậu tố để phân biệt.")
                continue
            VaiTro=input("Vai trò: ").strip().replace('|', '-')
            GiaStr=input("Đơn giá/giờ: ").replace('.', '').replace(',', '')
            try:
                P.ThanhVien.themPT(ThanhVien(Ten, VaiTro, float(GiaStr)))
                print("-> Đã thêm thành viên thành công!")
            except ValueError:
                print("Lỗi: Đơn giá không hợp lệ. Vui lòng nhập lại thông tin người này.")

def danhMucCongViec(Projects):
    print("\n--- KHỞI TẠO DANH MỤC CÔNG VIỆC  ---")
    P=nhapVaTimDuAn(Projects)
    if not P:
        return
    print("1. Nhập từ file CSV | 2. Nhập tay")
    Chon=input("Lựa chọn (1/2): ").strip()
    if Chon == "1":
        FileExcel=input("Nhập tên file danh mục (VD: danh_muc.csv): ").strip()
        if not os.path.exists(FileExcel):
            print("Lỗi: Không tìm thấy file!")
            return
        SoLuong=0
        DongDau=True
        with open(FileExcel, 'r', encoding='utf-8') as F:
            for L in F:
                L=L.strip()
                if not L:
                    continue
                if DongDau:
                    DongDau=False
                    continue
                K=ngatChuoi(L, ",")
                if len(K) >= 3:
                    MaCV=K.get(0).strip()
                    if timCV(P, MaCV):
                        print(f" ! Bỏ qua: Mã '{MaCV}' đã tồn tại.")
                        continue
                    TenCV=K.get(1).strip().replace('|', '-')
                    LoaiHinh=K.get(2).strip().replace('|', '-')
                    CongViecTruoc=""
                    if len(K) >= 4:
                        CongViecTruoc=K.get(3).strip().replace('|', '-')
                    TrangThai="Locked" if CongViecTruoc else "To Do"
                    NewCV=CongViec(MaCV, TenCV, LoaiHinh, CongViecTruoc, TrangThai)
                    P.DanhMucCV.themPT(NewCV)
                    SoLuong+=1
                    print(f" + Nạp thành công: {MaCV} - {TenCV} (Trạng thái: {TrangThai})")
        print(f"-> Hoàn tất: Đã nạp {SoLuong} hạng mục.")
    elif Chon == "2":
        print("Nhập thông tin các đầu việc. Nhập '0' tại Mã CV để hoàn tất.")
        while True:
            MaCV=input("\nMã công việc (VD: CV01) hoặc '0' để thoát: ").strip()
            if MaCV == '0' or MaCV == '':
                break
            if timCV(P, MaCV):
                print("Lỗi: Mã công việc đã tồn tại!")
                continue
            TenCV=input("Tên công việc: ").strip().replace('|', '-')
            LoaiHinh=input("Loại hình : ").strip().replace('|', '-')
            CongViecTruoc=input("Mã công việc yêu cầu làm trước (VD: CV01;CV02 hoặc Enter bỏ qua): ").strip().replace('|', '-')
            TrangThai="Locked" if CongViecTruoc else "To Do"
            NewCV=CongViec(MaCV, TenCV, LoaiHinh, CongViecTruoc, TrangThai)
            P.DanhMucCV.themPT(NewCV)
            print(f"-> Đã thêm vào danh mục (Trạng thái: {TrangThai})!")

def ghiNhanTimesheet(Projects):
    print("\n--- GHI NHẬN CHẤM CÔNG THEO NGÀY ---")
    P=nhapVaTimDuAn(Projects)
    if not P:
        return
    TgBdDuAn=datetime.strptime(P.TgBatDau, "%d/%m/%Y")
    TgKtDuAn=datetime.strptime(P.TgKetThuc, "%d/%m/%Y")
        
    print("1. Nhập từ file CSV | 2. Nhập tay từng lượt")
    Chon=input("Lựa chọn (1/2): ").strip()
    if Chon == "1":
        FileExcel=input("Nhập tên file chấm công (VD: cham_cong_cau.csv): ").strip()
        if not os.path.exists(FileExcel):
            print("Lỗi: Không tìm thấy file!")
            return
        SoLuong=0
        DongDau=True 
        with open(FileExcel, 'r', encoding='utf-8') as F:
            for L in F:
                L=L.strip()
                if not L:
                    continue
                if DongDau: 
                    DongDau=False
                    continue
                
                K=ngatChuoi(L, ",")
                if len(K) >= 7:
                    MaCV=K.get(0).strip()
                    NguoiThucHien=K.get(3).strip()
                    NgayStr=K.get(4).strip()
                    TrangThaiChuoi=K.get(6).strip().replace('|', '-')
                    
                    CvGoc=timCV(P, MaCV)
                    if not CvGoc:
                        print(f" ! Bỏ qua: Mã '{MaCV}' chưa có trong Danh mục.")
                        continue
                    if CvGoc.TrangThai.lower() == "done":
                        print(f" ! Bỏ qua: Công việc '{MaCV}' đã Đóng (Done).")
                        continue
                    if CvGoc.TrangThai.lower() == "locked":
                        Deps=CvGoc.CongViecYeuCau.split(';')
                        AllDone=True
                        TasksChuaXong=[]
                        for Dep in Deps:
                            Dep=Dep.strip()
                            if Dep:
                                DepTask=timCV(P, Dep)
                                if not DepTask:
                                    AllDone=False
                                    TasksChuaXong.append(f"{Dep} (Không tồn tại)")
                                elif DepTask.TrangThai.lower() != "done":
                                    AllDone=False
                                    TasksChuaXong.append(Dep)
                        if not AllDone:
                            print(f" ! Bỏ qua: '{MaCV}' đang BỊ KHÓA. Chờ hoàn thành: {', '.join(TasksChuaXong)}.")
                            continue
                        else:
                            CvGoc.TrangThai="To Do"

                    TvHienTai=timThanhVien(P, NguoiThucHien)
                    if not TvHienTai:
                        print(f" ! Bỏ qua: '{NguoiThucHien}' chưa thuộc dự án.")
                        continue
                        
                    try:
                        SoGio=float(K.get(5).strip())
                        if not (0 < SoGio <= 24):
                            print(f" ! Bỏ qua: Số giờ làm '{SoGio}' tại '{MaCV}' vô lý.")
                            continue
                        NgayObj=datetime.strptime(NgayStr, "%d/%m/%Y")
                        if not (TgBdDuAn <= NgayObj <= TgKtDuAn):
                            print(f" ! Bỏ qua: '{MaCV}' chấm công ngoài thời gian dự án.")
                            continue
                    except ValueError:
                        print(f" ! Bỏ qua: Lỗi định dạng tại '{MaCV}'.")
                        continue

                    TongGioTrongNgay=SoGio
                    for Nk in P.NhatKyCong:
                        if Nk.NguoiThucHien == NguoiThucHien and Nk.NgayChamCong == NgayStr:
                            TongGioTrongNgay+=Nk.SoGioLam
                    if TongGioTrongNgay > 24:
                        print(f" ! Bỏ qua: '{NguoiThucHien}' vượt quá 24h ngày {NgayStr}.")
                        continue
                        
                    TongChiPhi=0.0
                    for Nk in P.NhatKyCong:
                        T=timThanhVien(P, Nk.NguoiThucHien)
                        if T: TongChiPhi+=Nk.SoGioLam * T.DonGia
                    if TongChiPhi + (SoGio * TvHienTai.DonGia) > P.NganSach:
                        print(f" ! Bỏ qua: Ghi nhận tại '{MaCV}' gây thủng ngân sách.")
                        continue

                    TtLower=TrangThaiChuoi.lower()
                    if "done" in TtLower or "xong" in TtLower: TtChuan="Done"
                    elif "progress" in TtLower or "dang" in TtLower: TtChuan="In Progress"
                    else: TtChuan="To Do"

                    P.NhatKyCong.themPT(NhatKyChamCong(MaCV, NguoiThucHien, NgayStr, SoGio))
                    CvGoc.TrangThai=TtChuan
                    for Cv in P.DanhMucCV:
                        if Cv.TrangThai.lower() == "locked":
                            Deps = Cv.CongViecYeuCau.split(';')
                            AllDone = True
                            for Dep in Deps:
                                Dep = Dep.strip()
                                if Dep:
                                    DepTask = timCV(P, Dep)
                                    if not DepTask or DepTask.TrangThai.lower() != "done":
                                        AllDone = False
                                        break
                            if AllDone:
                                Cv.TrangThai = "To Do"
                    SoLuong+=1
        print(f"-> Hoàn tất: Ghi nhận {SoLuong} lượt chấm công từ file.")
    elif Chon == "2":
        MaCV=input("Mã công việc đang làm: ").strip()
        CvGoc=timCV(P, MaCV)
        if not CvGoc:
            print("Lỗi: Công việc không có trong Danh mục. Vui lòng thêm trước!")
            return
        if CvGoc.TrangThai.lower() == "done":
            print("Lỗi: Công việc này đã Đóng (Done). Không thể chấm công!")
            return
        if CvGoc.TrangThai.lower() == "locked":
            Deps=CvGoc.CongViecYeuCau.split(';')
            AllDone=True
            TasksChuaXong=[]
            for Dep in Deps:
                Dep=Dep.strip()
                if Dep:
                    DepTask=timCV(P, Dep)
                    if not DepTask:
                        AllDone=False
                        TasksChuaXong.append(f"{Dep} (Lỗi mã này không có trong dự án)")
                    elif DepTask.TrangThai.lower() != "done":
                        AllDone=False
                        TasksChuaXong.append(Dep)
            if not AllDone:
                print(f"Lỗi: Công việc đang BỊ KHÓA (Locked). Cần hoàn thành các task sau trước: {'; '.join(TasksChuaXong)}!")
                return
            else:
                CvGoc.TrangThai="To Do"

        Nguoi=input("Người thực hiện: ").strip()
        TvHienTai=timThanhVien(P, Nguoi)
        if not TvHienTai:
            print("Lỗi: Người này chưa thuộc dự án!")
            return
        NgayObj=nhapNgay("Ngày chấm công (DD/MM/YYYY): ")
        if not (TgBdDuAn <= NgayObj <= TgKtDuAn):
            print(f"Lỗi: Nằm ngoài thời gian dự án ({P.TgBatDau} đến {P.TgKetThuc})!")
            return
        Ngay=NgayObj.strftime("%d/%m/%Y")
        try:
            SoGio=float(input("Số giờ làm: "))
            if not (0 < SoGio <= 24):
                print("Lỗi: Giờ làm phải lớn hơn 0 và nhỏ hơn 24!")
                return
        except ValueError:
            print("Lỗi: Số giờ phải là số!")
            return
        TongGioTrongNgay=SoGio
        for Nk in P.NhatKyCong:
            if Nk.NguoiThucHien == Nguoi and Nk.NgayChamCong == Ngay:
                TongGioTrongNgay+=Nk.SoGioLam
        if TongGioTrongNgay > 24:
            print(f"Lỗi: '{Nguoi}' đã làm {TongGioTrongNgay - SoGio}h trong ngày. Vượt quá 24h/ngày!")
            return
        TongChiPhi=0.0
        for Nk in P.NhatKyCong:
            T=timThanhVien(P, Nk.NguoiThucHien)
            if T: TongChiPhi+=Nk.SoGioLam * T.DonGia
        if TongChiPhi + (SoGio * TvHienTai.DonGia) > P.NganSach:
            print(f"Lỗi: VƯỢT QUÁ NGÂN SÁCH (Hụt {TongChiPhi + (SoGio * TvHienTai.DonGia) - P.NganSach:,.0f} VND)!")
            return

        print("Cập nhật Trạng thái cho đầu việc này:")
        print("1. To Do (Chưa bắt đầu) | 2. In Progress (Đang thực hiện) | 3. Done (Đã hoàn thành)")
        ChonTt=input("Lựa chọn (1/2/3): ").strip()
        if ChonTt == "3": TtChuan="Done"
        elif ChonTt == "2": TtChuan="In Progress"
        else: TtChuan="To Do"
        CvGoc.TrangThai=TtChuan
        P.NhatKyCong.themPT(NhatKyChamCong(MaCV, Nguoi, Ngay, SoGio))
        print("-> Đã ghi nhận an toàn!")

def baoCaoDuAn(Projects):
    print("\n--- BÁO CÁO TỔNG HỢP DỰA TRÊN DANH MỤC VÀ TIMESHEET ---")
    P=nhapVaTimDuAn(Projects)
    if not P:
        return
    TongSoTaskKeHoach=len(P.DanhMucCV)
    TaskHoanThanh=0
    for Cv in P.DanhMucCV:
        if Cv.TrangThai.lower() == "done":
            TaskHoanThanh+=1
    TienDoPhanTram=(TaskHoanThanh / TongSoTaskKeHoach * 100) if TongSoTaskKeHoach > 0 else 0.0
    TongChiPhiNhanCong=0.0
    for Nk in P.NhatKyCong:
        Tv=timThanhVien(P, Nk.NguoiThucHien)
        MucGia=Tv.DonGia if Tv else 0.0
        TongChiPhiNhanCong+=Nk.SoGioLam * MucGia
    print("-" * 50)
    print(f"DỰ ÁN: {P.TenDA.upper()} | Khách hàng: {P.KhachHang}")
    print(f"Ngân sách phê duyệt: {P.NganSach:,.0f} VND")
    print(f"Thời gian: {P.TgBatDau} -> {P.TgKetThuc}")
    print("-" * 50)
    
    print("1. TIẾN ĐỘ CÔNG VIỆC THỰC TẾ:")
    print(f"   - Tổng số đầu việc cần làm        : {TongSoTaskKeHoach}")
    print(f"   - Số đầu việc đã xong (Done)      : {TaskHoanThanh}")
    print(f"   => Tỷ lệ hoàn thành               : {TienDoPhanTram:.2f}%")
    
    print("\n2. TÀI CHÍNH VÀ NGUỒN LỰC:")
    print(f"   - Tổng số lượt đã chấm công       : {len(P.NhatKyCong)}")
    print(f"   - Tổng tiền công đã trả hiện tại  : {TongChiPhiNhanCong:,.0f} VND")
    
    NganSachConLai=P.NganSach - TongChiPhiNhanCong
    if NganSachConLai >= 0:
        print(f"   => TRẠNG THÁI AN TOÀN (Còn dư {NganSachConLai:,.0f} VND)")
    else:
        print(f"   => CẢNH BÁO: VƯỢT QUÁ NGÂN SÁCH ( {-NganSachConLai:,.0f} VND)")
    print("-" * 50)

def main():
    taoFileKhoiDong()
    Projects=capNhatDuLieu()
    while True:
        print("\n" + "="*50)
        print("  HỆ THỐNG QUẢN LÝ CÔNG VIỆC DỰ ÁN ")
        print("="*50)
        print("1. Tạo mới dự án")
        print("2. Thêm nhân sự vào dự án")
        print("3. Khởi tạo Danh mục công việc")
        print("4. Ghi nhận chấm công hàng ngày (Timesheet)")
        print("5. Xuất báo cáo tổng hợp (Tiến độ và Chi phí)")
        print("6. Đồng bộ lưu dữ liệu và Thoát")
        print("="*50)
        LuaChon=input("Nhập lựa chọn (1-6): ").strip()
        
        if LuaChon == "1":
            taoDuAn(Projects)
        elif LuaChon == "2":
            themThanhVien(Projects)
        elif LuaChon == "3":
            danhMucCongViec(Projects)
        elif LuaChon == "4":
            ghiNhanTimesheet(Projects)
        elif LuaChon == "5":
            baoCaoDuAn(Projects)
        elif LuaChon == "6":
            luuDuLieu(Projects)
            print("Đã lưu dữ liệu thành công. Tạm biệt!")
            break
        else:
            print("Lỗi: Vui lòng chọn từ 1 đến 6.")

if __name__ == "__main__":
    main()
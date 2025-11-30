import numpy as np
import matplotlib.pyplot as plt

# --- 1. HÀM MỤC TIÊU ---
def sphere_function(x):
    return np.sum(x**2)

# --- 2. HÀM GWO ---
def GWO(obj_func, lb, ub, dim, pop_size, max_iter):
    
    # Khởi tạo quần thể
    positions = np.random.uniform(0, 1, (pop_size, dim)) * (ub - lb) + lb
    
    # Khởi tạo Alpha, Beta, Delta
    Alpha_pos = np.zeros(dim)
    Alpha_score = float("inf")
    
    Beta_pos = np.zeros(dim)
    Beta_score = float("inf")
    
    Delta_pos = np.zeros(dim)
    Delta_score = float("inf")
    
    # Mảng lưu lịch sử để vẽ biểu đồ
    convergence_curve = []

    print(f"\n=> Đang khởi chạy GWO với: Dim={dim}, Pop={pop_size}, Iter={max_iter}")
    print("-" * 40)

    # Vòng lặp chính
    for t in range(0, max_iter):
        
        for i in range(0, pop_size):
            positions[i,:] = np.clip(positions[i,:], lb, ub)
            fitness = obj_func(positions[i,:])
            
            if fitness < Alpha_score:
                Alpha_score = fitness
                Alpha_pos = positions[i,:].copy()
            elif fitness < Beta_score:
                Beta_score = fitness
                Beta_pos = positions[i,:].copy()
            elif fitness < Delta_score:
                Delta_score = fitness
                Delta_pos = positions[i,:].copy()
        
        # Lưu lại giá trị tốt nhất của vòng lặp này
        convergence_curve.append(Alpha_score)

        a = 2 - t * (2 / max_iter)
        
        for i in range(0, pop_size):
            for j in range(0, dim):
                r1, r2 = np.random.random(), np.random.random()
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                D_alpha = abs(C1 * Alpha_pos[j] - positions[i, j])
                X1 = Alpha_pos[j] - A1 * D_alpha
                
                r1, r2 = np.random.random(), np.random.random()
                A2 = 2 * a * r1 - a
                C2 = 2 * r2
                D_beta = abs(C2 * Beta_pos[j] - positions[i, j])
                X2 = Beta_pos[j] - A2 * D_beta
                
                r1, r2 = np.random.random(), np.random.random()
                A3 = 2 * a * r1 - a
                C3 = 2 * r2
                D_delta = abs(C3 * Delta_pos[j] - positions[i, j])
                X3 = Delta_pos[j] - A3 * D_delta
                
                positions[i, j] = (X1 + X2 + X3) / 3
    
    return Alpha_score, Alpha_pos, convergence_curve

# --- 3. CHẠY VÀ VẼ BIỂU ĐỒ (Đã sửa để nhận Input) ---
if __name__ == "__main__":
    print("=== CẤU HÌNH THAM SỐ GWO ===")
    print("(Nhấn Enter để dùng giá trị mặc định)")
    
    try:
        # 1. Nhập số chiều (Dimension)
        d_in = input("1. Nhập số chiều (Mặc định 30): ")
        dim = int(d_in) if d_in.strip() else 30
        
        # 2. Nhập số lượng sói (Population)
        p_in = input("2. Nhập số lượng sói (Mặc định 50): ")
        pop_size = int(p_in) if p_in.strip() else 50
        
        # 3. Nhập số vòng lặp (Iterations)
        i_in = input("3. Nhập số vòng lặp (Mặc định 100): ")
        max_iter = int(i_in) if i_in.strip() else 100
        
    except ValueError:
        print("\n[LỖI] Bạn nhập không phải số! Chương trình sẽ dùng cấu hình mặc định.")
        dim = 30
        pop_size = 50
        max_iter = 100

    # Các tham số cố định khác
    lb = -100
    ub = 100

    # Chạy thuật toán
    best_score, best_pos, curve = GWO(sphere_function, lb, ub, dim, pop_size, max_iter)

    # In kết quả
    print("-" * 40)
    print(f"KẾT QUẢ CUỐI CÙNG:")
    print(f"Best Score: {best_score}")
    print(f"Best Position (rút gọn): {best_pos[:5]} ...")
    print("-" * 40)

    # --- VẼ BIỂU ĐỒ MATLAB STYLE ---
    plt.figure(figsize=(10, 6))
    plt.semilogy(curve, 'b-', linewidth=2) 
    
    # Cập nhật tiêu đề biểu đồ để hiển thị tham số đã nhập
    plt.title(f'GWO Convergence (Dim={dim}, Pop={pop_size}, Iter={max_iter})')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness Value (Log Scale)')
    plt.grid(True)
    plt.show()
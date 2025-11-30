import numpy as np
import matplotlib.pyplot as plt

# 1. HÀM MỤC TIÊU (SPHERE FUNCTION)
def sphere_function(x):
    return np.sum(x**2)

# 2. THUẬT TOÁN GWO
def GWO(search_agents_no, max_iter, dim, lb, ub):
    # Khởi tạo quần thể
    positions = np.random.uniform(0, 1, (search_agents_no, dim)) * (ub - lb) + lb
    
    # Khởi tạo Alpha, Beta, Delta
    Alpha_pos = np.zeros(dim)
    Alpha_score = float("inf")
    
    Beta_pos = np.zeros(dim)
    Beta_score = float("inf")
    
    Delta_pos = np.zeros(dim)
    Delta_score = float("inf")
    
    convergence_curve = [] # Lưu lịch sử để vẽ biểu đồ

    for t in range(0, max_iter):
        # Cập nhật Alpha, Beta, Delta
        for i in range(0, search_agents_no):
            positions[i,:] = np.clip(positions[i,:], lb, ub)
            fitness = sphere_function(positions[i,:])
            
            if fitness < Alpha_score:
                Alpha_score = fitness
                Alpha_pos = positions[i,:].copy()
            elif fitness < Beta_score:
                Beta_score = fitness
                Beta_pos = positions[i,:].copy()
            elif fitness < Delta_score:
                Delta_score = fitness
                Delta_pos = positions[i,:].copy()
        
        # Cập nhật vị trí các con sói
        a = 2 - t * (2 / max_iter) # a giảm từ 2 xuống 0
        
        for i in range(0, search_agents_no):
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
        
        convergence_curve.append(Alpha_score)
        
    return convergence_curve, Alpha_score

# 3. THIẾT LẬP THAM SỐ CHUNG
dim = 30
lb = -100
ub = 100

# --- KỊCH BẢN 1: TÀI NGUYÊN THẤP (V1) ---
# Ít sói, ít vòng lặp -> Chạy nhanh nhưng kém chính xác
pop_v1 = 5
iter_v1 = 30 
curve_v1, score_v1 = GWO(pop_v1, iter_v1, dim, lb, ub)

# --- KỊCH BẢN 2: TÀI NGUYÊN CAO (V2) ---
# Nhiều sói, nhiều vòng lặp -> Chạy lâu hơn nhưng chính xác cao
pop_v2 = 50
iter_v2 = 100 
curve_v2, score_v2 = GWO(pop_v2, iter_v2, dim, lb, ub)

# 4. VẼ BIỂU ĐỒ SO SÁNH
plt.figure(figsize=(10, 6))

# Vẽ đường V1
# Dùng semilogy (trục log) để nhìn rõ sự khác biệt khi giá trị về rất nhỏ
plt.semilogy(curve_v1, color='red', linestyle='-', linewidth=2, label=f'V1: Low Res (Pop={pop_v1}, Iter={iter_v1})')

# Vẽ đường V2
plt.semilogy(curve_v2, color='blue', linestyle='-', linewidth=2, label=f'V2: High Res (Pop={pop_v2}, Iter={iter_v2})')

plt.title('Comparison of GWO Convergence (Sphere Function)')
plt.xlabel('Iteration (Vòng lặp)')
plt.ylabel('Best Score (Log scale)')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)

# Hiển thị kết quả ra màn hình console
print(f"Kết quả V1 (Low): {score_v1}")
print(f"Kết quả V2 (High): {score_v2}")
print(f"V2 tốt hơn V1 khoảng: {score_v1/score_v2:.2e} lần")

plt.show()
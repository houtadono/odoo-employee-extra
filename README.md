1. Kế thừa Model Employee (Nâng cao)
   - Tạo field "years_of_experience" kiểu Integer.
   - Tạo bảng certifications, skills, và các bảng liên quan: employee_skills, certifications_skills, skills_level, skills_type.
   
2. Tạo Wizard
   - Tạo Wizard cho phép người dùng cập nhật nhiều certifications, kĩ năng kèm theo cho nhiều nhân viên. 

3. Phân quyền nâng cao
   - Tạo các nhóm quyền riêng biệt:
      - Employee Experience Manager : Quản lí trường years_of_experience, tự động cập nhật dựa trên skill
      - Employee Skills Manager : Quản lí Skill, Skill Type, Skill Level
      - Employee Certifications Manager : Quản lí Certification

4. Kế thừa quyền
   - Nhóm quyền "Employee Experience Manager Extend" kế thừa 3 nhóm quyền trên, ngoài ra có khả năng tới quyền quản lí các employee-skill, employee-certification. Tuy nhiên có 1 số hạn chế:
      - Có thể create, unlink nhưng không đc phép sửa các employee-skill mà không thuộc 1 chứng chỉ nào của employee đó. 
      - Không thể xóa skill khi skill đó có người đang có.
   - Nhóm quyền Administrator với id "hr.group_hr_manager" được kế thừa thêm nhóm quyền "Employee Experience Manager Extend" và không có hạn chế. 

5. Kế thừa view
   - Kế thừa form view của hr.employee hợp lí, hiển thị wizard, skill, certification dựa trên quyền.
   
6. Thêm smartbutton
   - Smartbutton cho phép cập nhật skill dựa trên chứng chỉ đạt được với 2 tùy chọn: 
      - Chỉ giữ các skill tốt nhất trong chứng chỉ
      - Giữ lại hết cả skill tốt bên ngoài chứng chỉ 

7. Xử lý record
   - Kế thừa lại create, write xử lý tự động cập nhật kỹ năng khi thêm chứng chỉ, có option tự động cập nhật years_of_exp theo skill và đưa ra cảnh báo khi years_of_exp > 30.

1. Kế thừa Model Employee
   - Tạo field "years_of_experience" kiểu Integer.
2. Tạo Wizard
   - Tạo Wizard cho phép người dùng cập nhật "years_of_experience" cho nhiều nhân viên. 
3. Thêm quyền mới
   - Tạo nhóm quyền "Employee Experience Manager".
   - Set nhóm vừa tạo vào quyền của field "years_of_experience" trong model kế thừa. 
4. Kế thừa quyền
   - Tạo nhóm quyền "Employee Experience Manager Extend" implied "Employee Experience Manager".
   - Set nhóm vừa tạo vào quyền của field "parent_id" và "job_id" trong view kế thừa.
   - Mặc định user_root, user_admin có nhóm quyền này.
5. Kế thừa view
   - Thêm trường years_of_experience vào vị trí hợp lý
6. Thêm smartbutton
   - Smartbutton thực hiện mở action tương tự của wizard 2. bên trên nhưng truyền các default context xử lý bản ghi hiện tại. 
7. Xử lý record
   - Kế thừa lại create, write kiểm tra 0<=year_of_experience<=30     

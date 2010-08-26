==============
Inforlearn.com
==============

Mã nguồn
========

  * Mã nguồn sản phẩm được cập nhật tại địa chỉ::
      
      http://github.com/AloneRoad/Inforlearn


Hướng dẫn nhanh
===============

Chạy thử sản phẩm
-----------------

  1. Lấy một bản sao của toàn bộ mã nguồn đang phát triển về máy::
  
      git clone git://github.com/AloneRoad/Inforlearn.git
    
  2. Khởi chạy ứng dụng::
  
      ./start.sh  
    
  3. Truy cập ứng dụng tại địa chỉ::
  
      http://localhost:8080/
    
    
Triển khai ứng dụng với Google App Engine
-----------------------------------------

  1. Đăng ký một tài khoản và tạo một ứng dụng tại http://appspot.com
  
  2. Lấy toàn bộ mã nguồn đang phát triển về máy
  
  3. Sửa ID của ứng dụng thành ID bạn vừa đăng ký trong file app.yaml (dòng đầu tiên)

  4. Chuyển code lên Google App Engine::
    
      ./update.sh
      
  5. Truy cập dòng lệnh điều khiển ứng dụng đang chạy::
      
      ./console.sh



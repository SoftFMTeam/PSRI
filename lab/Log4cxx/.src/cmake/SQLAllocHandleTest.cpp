// SQLAllocHandleTest.cpp
// compile with: odbc32.lib user32.lib
#include <windows.hpp>
#include <sqlext.hpp>

int main() {
   SQLHENV henv;
   SQLRETURN retcode;

   retcode = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
   if (retcode == SQL_SUCCESS || retcode == SQL_SUCCESS_WITH_INFO) {
       SQLFreeHandle(SQL_HANDLE_ENV, henv);
   }
   return 1;
}
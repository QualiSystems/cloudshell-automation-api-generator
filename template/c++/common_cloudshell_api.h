#ifndef QUALISYSTEMS_CLOUDSHELL_API_COMMON_CLOUDSHELL_API_H_
#define QUALISYSTEMS_CLOUDSHELL_API_COMMON_CLOUDSHELL_API_H_

#include <string>
#include <map>

namespace qualisystems {
    class CommonAPISession {
    public:
        CommonAPISession(const std::string& host, const std::string& username,
                         const std::string& password, const std::string& domain);
        virtual ~CommonAPISession();

    protected:
        virtual std::string sendRequest(const std::string& operation, const std::string& message,
                                const std::string& request_headers);

        virtual std::string generateAPIRequest(const std::map<std::string, std::string>& args_map);

    protected:
        std::string host_;
        std::string username;
        std::string password;
        std::string domain;

        std::map<std::string, std::string> headers_;
    };
}

#endif
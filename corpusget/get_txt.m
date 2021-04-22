%% -------------------------------------------------------------------
% Descrption : Web file crawler
% Author : Wang Kang
% Mail : goto.champion@gmail.com
% Blog : kang.blog.com
%% -------------------------------------------------------------------
website = 'http://www.gutenberg.org/browse/languages/ru'; % the website you wanna crawling
filetypes = {'txt'}; % the file your wanna download during crawling
downloadPath = uigetdir; % where to download
if ~isdir(downloadPath)
    mkdir(downloadPath);
end

% start crawling
crawling(website, filetypes, downloadPath)


sss = getGoodSubjects();
for glm = 98:101
    for subj = sss  %sss
        for run = 1:9 %  1:9
            multi = context_create_multi(glm, subj, run);
        end
    end
end

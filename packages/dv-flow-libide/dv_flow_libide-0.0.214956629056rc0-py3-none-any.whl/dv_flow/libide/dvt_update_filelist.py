import os
from dv_flow.mgr import TaskDataInput, TaskRunCtxt

async def UpdateFileList(ctxt : TaskRunCtxt, input : TaskDataInput):

    changed = input.changed

    if not os.path.isdir(os.path.join(ctxt.root_pkgdir, ".dvt")):
        os.makedirs(os.path.join(ctxt.root_pkgdir, ".dvt"))

    fp = open(os.path.join(ctxt.root_pkgdir, ".dvt/default.build"), "w")


    incdirs = set()

    for fs in input.inputs:
        fp.write("# Files from task %s\n" % fs.src)
        if hasattr(fs, "incdirs"):
            for d in fs.incdirs:
                incdir = os.path.join(fs.basedir, d)
                if incdir not in incdirs:
                    incdirs.add(os.path.join(fs.basedir, d))
                    fp.write("+incdir+%s\n" % os.path.join(fs.basedir, d))

        if hasattr(fs, "files"):
            for f in fs.files:
                incdir = os.path.dirname(os.path.join(fs.basedir, f))
                if incdir not in incdirs:
                    incdirs.add(incdir)
                    fp.write("+incdir+%s\n" % incdir)
                fp.write("%s\n" % os.path.join(fs.basedir, f))

        fp.write("\n")





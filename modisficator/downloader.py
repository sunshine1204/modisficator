#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ftplib
import time
import os
"""The downloader code downloads MODIS datasets from NASA's website.
"""
class invalid_platform(Exception):
    print "The platform you selected is not TERRA, AQUA or COMBINED"

class invalid_product(Exception):
    print "The product you selected does not appear to exist."


class downloader:
    
    def __init__ ( self, tile, collection="005" ):
        """
        For some reason, I put something about the collection there, which is not
        yeat in the database.
        """
        self.ftp_host = "e4ftl01u.ecs.nasa.gov"
        self.ftp = ftplib.ftp ( self.ftp_host )
        self.ftp.login()
        self.collection = collection
        self.tile = tile

    def get_product ( self, product_name, start_date, platform, \
                        end_date=None):
        """
        This is the method that does the downloading of a prdouct
        """
        platform_dir = {"TERRA":"/MOLT/", "AQUA":"/MOLA/", \
                    "COMBINED":"/MOTA/"}
        if not platform_dir.has_key(platform):
            raise invalid_platform, "Your platform was %s"%platform
        
        try:
            self.ftp.cwd ("/%s/%s.%s/"%( platform_dir[platform], \
                            product_name, self.collection ))
        except error_perm:
            raise invalid_product, "This product doesn't seem to exist?"
        dates = []
        def parse(line):
            if line[0] == 'd':
                dates.append(line.rpartition(' ')[2])   
        self.ftp.dir( parse )
        dates.sort()
        Dates = [ time.strptime(d, "%Y.%m.%d") for d in dates ]
        try:
            istart = [ i for i in xrange(len(Dates)) \
                    if Dates[i] == start_date ][0]
        except:
            raise ValueError, "Wrong start date!"
        
        if end_date != None:
            try:
                iend = [ i for i in xrange(len(Dates)) \
                    if (Dates[i]>=start_date) and ( Dates[i]<=end_date) ][0]
            except:
                raise ValueError, "Wrong end date!"
            get_dates = dates[istart:iend]
        else:
            get_dates = list ( dates[istart] )
        out_dir = os.path.join ( self.output_dir, platform, product, self.tile )
        if not os.path.exists ( out_dir ):
            os.makedirs ( out_dir )
        for fecha in get_dates:
            self.ftp.cwd ( "%s"%fecha )
            fichs = []
            self.ftp.list ( fichs.append )
            grab = [ f for f in fichs if f.find( self.tile ) >= 0 ]
            for grab_file in grab:
                fname = grab_file.split()[7]
                out_dir 
                f_out = open( os.path.join ( out_dir, fname), 'wb')
                # Download the file a chunk at a time
                # Each chunk is sent to handleDownload
                # RETR is an FTP command
                print 'Getting ' + filename
                #
                def handle_download(block):
                    f_out.write(block)
                    
                self.ftp.retrbinary('RETR ' + fname, handle_download )
                f_out.close()

package com.sstickers.app;
import android.content.*; import android.database.*; import android.net.Uri; import android.os.*; import android.provider.OpenableColumns; import java.io.*;
public class StickerProvider extends ContentProvider {
 public boolean onCreate(){return true;}
 private String name(Uri uri){String s=uri.getLastPathSegment(); if(s==null||!s.matches("[0-9]{4}\\.png")) throw new IllegalArgumentException("Invalid sticker"); return s;}
 public String getType(Uri uri){return "image/png";}
 public Cursor query(Uri uri,String[] p,String s,String[] a,String o){String n=name(uri); String[] cols=p==null?new String[]{OpenableColumns.DISPLAY_NAME,OpenableColumns.SIZE}:p; MatrixCursor c=new MatrixCursor(cols); Object[] row=new Object[cols.length]; long size=0; try(InputStream in=getContext().getAssets().open("stickers/"+n)){size=in.available();}catch(IOException ignored){} for(int i=0;i<cols.length;i++){if(OpenableColumns.DISPLAY_NAME.equals(cols[i]))row[i]="S-Sticker-"+n;else if(OpenableColumns.SIZE.equals(cols[i]))row[i]=size;} c.addRow(row);return c;}
 public ParcelFileDescriptor openFile(Uri uri,String mode)throws FileNotFoundException{if(!"r".equals(mode))throw new FileNotFoundException("Read only"); String n=name(uri); try{ParcelFileDescriptor[] pipe=ParcelFileDescriptor.createPipe(); new Thread(()->{try(InputStream in=getContext().getAssets().open("stickers/"+n); OutputStream out=new ParcelFileDescriptor.AutoCloseOutputStream(pipe[1])){byte[] b=new byte[8192]; int k; while((k=in.read(b))!=-1)out.write(b,0,k);}catch(IOException ignored){}}).start();return pipe[0];}catch(IOException e){throw new FileNotFoundException(n);}}
 public Uri insert(Uri u,ContentValues v){throw new UnsupportedOperationException();} public int delete(Uri u,String s,String[] a){throw new UnsupportedOperationException();} public int update(Uri u,ContentValues v,String s,String[] a){throw new UnsupportedOperationException();}
}
